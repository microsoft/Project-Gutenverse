# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from loguru import logger
from stage import Stage
from config import config
from PIL import Image
from rembg import remove
import json
import os
from llm import *

class SkyboxGen:
    def __repr__(self) -> str:
        return 'SkyboxGenStage'

    def __str__(self) -> str:
        return self.__repr__()

    def process(self, context, image_gen_llm):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)

        # For each subfolder in the story_folder
        for subfolder in sorted(os.listdir(story_folder)):
            subfolder_path = os.path.join(story_folder, subfolder)

            save_file_path = os.path.join(subfolder_path, '3_skyboxgen_stage.json')
            if os.path.isfile(save_file_path):
                logger.info(f"{self} step found to be already completed for scene " + subfolder)
                continue
            
            # Check if the path is a directory and contains the required JSON file
            if os.path.isdir(subfolder_path) and '1_analysis_stage.json' in os.listdir(subfolder_path):
                json_path = os.path.join(subfolder_path, '1_analysis_stage.json')
                
                # Read the JSON file
                with open(json_path, 'r') as file:
                    data = json.load(file)
                    setting = data.get('setting', {})
                    skybox_gen_data = {"skybox": {}}
                    visual_style = data.get('visualstyle', '')
                    skybox_prompt = ", ".join([setting["location"],
                                             setting["timeofday"],
                                             setting["weather"],
                                             setting["visualelements"],
                                             "masterpiece",
                                             visual_style])

                    flat_skybox_name = self.generate_image(subfolder_path, "skybox", skybox_prompt, image_gen_llm)
                    image_filepath = self.create_pseudo_360(subfolder_path, flat_skybox_name, os.path.join(subfolder_path, "skybox_360.png"))
                    skybox_gen_data = {
                        "setting_info": setting,
                        "prompt": skybox_prompt,
                        "image": image_filepath
                    }
                    
                    # Save the aggregated data to a new JSON file in the current subfolder
                    with open(save_file_path, 'w') as output_file:
                        json.dump(skybox_gen_data, output_file, indent=4)

        return context

    def generate_image(self, subfolder_path, skybox_name, appearance, image_gen_llm):
        filename = f"{skybox_name.replace(' ', '')}.png"
        prompt = appearance
        negative_prompt = "low quality"

        if (config.UseGpuImageGen):
            image = image_gen_llm.generate(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=512)
        else:
            image = image_gen_llm.generate(prompt=prompt, negative_prompt=negative_prompt, width=512, height=512)

        imagePath = os.path.join(subfolder_path, filename)
        image.save(imagePath)
        return filename
    
    def create_pseudo_360(self, subfolder_path, skybox_filename, output_path):
        # Open the image
        imagePath = os.path.join(subfolder_path, skybox_filename)
        image = Image.open(imagePath)
        original_width, original_height = image.size
        
        # flip twice if not using GpuImageGen because image width is only 512
        times_to_flip = 1
        if not config.UseGpuImageGen:
            times_to_flip = 2

        for _ in range(times_to_flip):
            # Flip the image and append to the right
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            new_width = original_width * 2
            new_image = Image.new("RGB", (new_width, original_height))
            new_image.paste(image, (0, 0))
            new_image.paste(flipped_image, (original_width, 0))

            # update width and image
            if times_to_flip > 1:
                image = new_image
                original_width = new_width
        
        # Add padding to the top and bottom
        top_padding = int(original_height * 0.2)
        bottom_padding = int(original_height * 0.6)
        padded_height = original_height + top_padding + bottom_padding
        final_image = Image.new("RGB", (new_width, padded_height), (0, 0, 0))
        final_image.paste(new_image, (0, top_padding))
        
        # Save the final image
        final_image.save(output_path)