from loguru import logger
from stage import Stage
from config import config
import json
import os

class SceneCompilationStage(Stage):
    def __repr__(self) -> str:
        return 'SceneCompilationStage'

    def __str__(self) -> str:
        return self.__repr__()

    def _process(self, context):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)
        
        scenes_json = {
            "title": context.title,
            "scenes": []
        }

        # For each subfolder in the story_folder
        for subfolder in sorted(os.listdir(story_folder)):
            if not os.path.isdir(os.path.join(story_folder, subfolder)):
                continue
            subfolder_path = os.path.join(story_folder, subfolder)

            save_file_path = os.path.join(subfolder_path, '5_scenecompilation_stage.json')
            if os.path.isfile(save_file_path):
                logger.info(f"{self} step found to be already completed for " + subfolder)
                continue
            
            segmentation_filepath = os.path.join(story_folder, subfolder, "scene.json")
            charactergen_filepath = os.path.join(story_folder, subfolder, "2_charactergen_stage.json")
            composition_filepath = os.path.join(story_folder, subfolder, "4_composition_stage.json")
            skybox_filepath = f"/stories/{str(context.id)}/{subfolder}/assets/skybox_360.png"
        
            if not os.path.isfile(charactergen_filepath):
                logger.info(f"{self} no character generation output found for " + subfolder + " skipping scene compilation")
                continue

            if not os.path.isfile(composition_filepath):
                logger.info(f"{self} no composition output found for " + subfolder + " skipping scene compilation")
                continue

            segmentation_data = self.load_json_data(segmentation_filepath)
            charactergen_data = self.load_json_data(charactergen_filepath, "characters")
            composition_data = self.load_json_data(composition_filepath, "characters")
            # add image from character gen object
            for character_name, character_info in charactergen_data.items():
                composition_data[character_name]['imageUrl'] = f"/stories/{str(context.id)}/{subfolder}/assets/{character_info.get('image')}"

            # set scene story text under 'narrator' character for now
            # since it is not broken down by speaker / not every story will have dialog
            # exclusively from characters
            composition_data["content"] = segmentation_data.get("content")
            scene_compilation_data = self.transform_composition_data(composition_data)
            
            scene_compilation_data["environment"] = skybox_filepath
            scene_json = scene_compilation_data

            # Save the aggregated data to a new JSON file in the current subfolder
            with open(save_file_path, 'w') as output_file:
                json.dump(scene_compilation_data, output_file, indent=4)
            
            scenes_json["scenes"].append(scene_json)

        with open(os.path.join(story_folder, "scene_compilation.json"), 'w') as output_file:
            json.dump(scenes_json, output_file, indent=4)

        return context

    
    def transform_composition_data(self, composition_data):
        transformed_characters = []

        for character_name, character_info in composition_data.items():
            # Check if character_info is not None
            if character_info is None:
                continue
            
            transformed_character = {
                "name": character_name,
                "distanceFromCamera": 60  # Default value
            }
            
            # Conditionally assign values if they exist in character_info
            if "distance_from_the_center_in_degree" in character_info:
                transformed_character["angularDistanceFromCamera"] = character_info["distance_from_the_center_in_degree"]
            if "scale_x" in character_info:
                transformed_character["width"] = character_info["scale_x"]
            if "scale_y" in character_info:
                transformed_character["height"] = character_info["scale_y"]
            if "distance_from_the_floor" in character_info:
                transformed_character["distanceFromGround"] = character_info["distance_from_the_floor"]
            if "imageUrl" in character_info:
                transformed_character["imageUrl"] = character_info["imageUrl"]

            transformed_characters.append(transformed_character)

        transformed_data = {
            "characters": transformed_characters,
            "speech": [
                {
                    "character": "narrator",
                    "text": composition_data["content"]
                }
            ]            
        }
        return transformed_data

    def load_json_data(self, filepath, rootNodeName = None):
        if not os.path.isfile(filepath):
            logger.error(f"{self} file not found at " + filepath)

        with open(filepath, 'r') as file:
                data = json.load(file)
                if rootNodeName is not None:
                    json_data = data.get(rootNodeName, {})
                else:
                    json_data = data
                return json_data
