from loguru import logger
from stage import Stage
from config import config
from rembg import remove
import json
import os
from kandinskyllm import KandinskyLLM

class SkyboxGenStage(Stage):
    def __init__(self) -> None:
        self.imageGenLLM = KandinskyLLM()
        super().__init__()

    def __repr__(self) -> str:
        return 'SkyboxGenStage'

    def __str__(self) -> str:
        return self.__repr__()


    def _process(self, context):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)

        # For each subfolder in the story_folder
        for subfolder in sorted(os.listdir(story_folder)):
            subfolder_path = os.path.join(story_folder, subfolder)

            save_file_path = os.path.join(subfolder_path, '3_skyboxgen_stage.json')
            if os.path.isfile(save_file_path):
                logger.info(f"{self} step found to be already completed")
                return context
            
            # Check if the path is a directory and contains the required JSON file
            if os.path.isdir(subfolder_path) and '1_analysis_stage.json' in os.listdir(subfolder_path):
                json_path = os.path.join(subfolder_path, '1_analysis_stage.json')
                
                # Read the JSON file
                with open(json_path, 'r') as file:
                    data = json.load(file)
                    setting = data.get('setting', {})
                    skybox_gen_data = {"skybox": {}}
                    
                    skybox_prompt = " ".join([setting["location"],
                                             setting["timeofday"],
                                             setting["weather"],
                                             setting["visualelements"],
                                             "beautiful",
                                             "stunning"])

                    image_filepath = self.generate_image(subfolder_path, "0_skybox", skybox_prompt)
                    skybox_gen_data = {
                        "setting_info": setting,
                        "prompt": skybox_prompt,
                        "image": image_filepath
                    }
                    
                    # Save the aggregated data to a new JSON file in the current subfolder
                    with open(save_file_path, 'w') as output_file:
                        json.dump(skybox_gen_data, output_file, indent=4)

        return context

    def generate_image(self, subfolder_path, skybox_name, appearance):
        filename = f"{skybox_name.replace(' ', '')}.png"
        prompt = appearance
        negative_prompt = "low quality"
        image = self.imageGenLLM.generate(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=512)
        imagePath = os.path.join(subfolder_path, filename)
        image_bg_removed = remove(image)
        image_bg_removed.save(imagePath)
        return filename