import json
import os

from loguru import logger
from config import config
from transparent_background import Remover
from llm import *

class CharacterGen:
    def __repr__(self) -> str:
        return 'CharacterGenStage'

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self):
        self.remover = Remover()

    def process(self, context, image_gen_llm):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)

        # For each subfolder in the story_folder
        for subfolder in sorted(os.listdir(story_folder)):
            subfolder_path = os.path.join(story_folder, subfolder)

            save_file_path = os.path.join(subfolder_path, '2_charactergen_stage.json')
            if os.path.isfile(save_file_path):
                logger.info(f"{self} step found to be already completed for " + subfolder)
                continue
            
            # Check if the path is a directory and contains the required JSON file
            if os.path.isdir(subfolder_path) and '1_analysis_stage.json' in os.listdir(subfolder_path):
                json_path = os.path.join(subfolder_path, '1_analysis_stage.json')
                
                # Read the JSON file
                with open(json_path, 'r') as file:
                    data = json.load(file)
                    characters = data.get('characters', {})
                    visual_style = data.get('visualstyle', '')
                    character_gen_data = {"characters": {}}
                    
                    # For each character in the JSON
                    for character_name, description in characters.items():
                        appearance = ''
                        summary = ''
                        # Support both old and new JSON formats
                        if type(description) is dict:
                            appearance = description.get('appearance', '')
                            summary = description.get('summary', '')
                        else:
                            appearance = summary = description
                        appearance += ', full body'
                        appearance += ', ' + visual_style
                        image_filepath = self.generate_image(subfolder_path, character_name, appearance, image_gen_llm)
                        character_gen_data['characters'][character_name] = {
                            "summary": summary,
                            "appearance": appearance,
                            "image": image_filepath
                        }
                    
                    # Save the aggregated data to a new JSON file in the current subfolder
                    with open(save_file_path, 'w') as output_file:
                        json.dump(character_gen_data, output_file, indent=4)
            

        return context

    def generate_image(self, subfolder_path, character_name, appearance, image_gen_llm):
        filename = f"character_{character_name.replace(' ', '')}.png"
        prompt = appearance
        negative_prompt = "bad anatomy, low quality, blurred, blurry edges, incomplete body"
        image = image_gen_llm.generate(prompt=prompt, negative_prompt=negative_prompt)
        imagePath = os.path.join(subfolder_path, filename)
        image_bg_removed = Image.fromarray(self.remover.process(image))
        image_bg_removed.save(imagePath)
        return filename
