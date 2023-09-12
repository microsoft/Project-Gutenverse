
from stage import Stage
from config import config
import json
import os

class CharacterGenStage(Stage):
    def __init__(self):
        pass

    def process(self, context):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)
        
        # For each subfolder in the story_folder
        for subfolder in sorted(os.listdir(story_folder)):
            subfolder_path = os.path.join(story_folder, subfolder)
            
            # Check if the path is a directory and contains the required JSON file
            if os.path.isdir(subfolder_path) and '1_analysis_stage.json' in os.listdir(subfolder_path):
                json_path = os.path.join(subfolder_path, '1_analysis_stage.json')
                
                # Read the JSON file
                with open(json_path, 'r') as file:
                    data = json.load(file)
                    characters = data.get('characters', {})
                    
                    character_gen_data = {"characters": {}}
                    
                    # For each character in the JSON
                    for character_name, description in characters.items():
                        image_filepath = self.generate_image(character_name, description)
                        character_gen_data['characters'][character_name] = {
                            "description": description,
                            "image": image_filepath
                        }
                    
                    # Save the aggregated data to a new JSON file in the current subfolder
                    with open(os.path.join(subfolder_path, '2_charactergen_stage.json'), 'w') as output_file:
                        json.dump(character_gen_data, output_file, indent=4)

    # placeholder method - replace with Sean's stable diffusion stuff
    def generate_image(self, character_name, description):
        # Return a filepath based on the character name by removing whitespace
        return f"{character_name.replace(' ', '')}.png"