
from stage import Stage
from config import config
import json
import os

class CompositionStage(Stage):
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
                    
                    character_composition_data = {"characters": {}}
                    
                    # For each character in the JSON
                    for character_name, description in characters.items():
                        #todo: fill in these values
                        
                        character_composition_data['characters'][character_name] = {
                            "distance_from_camera": 1,
                            "distance_from_the_floor": 0,
                            "distance_from_the_center_in_angle": 0,
                            "scale": 1,
                        }
                    
                    # Save the aggregated data to a new JSON file in the current subfolder
                    with open(os.path.join(subfolder_path, '3_composition_stage.json'), 'w') as output_file:
                        json.dump(character_composition_data, output_file, indent=4)
