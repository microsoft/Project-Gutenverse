from stage import Stage
from config import config
import json
import os
from llm import llm

class CompositionStage(Stage):

    def __repr__(self) -> str:
        return 'CompositionStage'

    def __str__(self) -> str:
        return self.__repr__()

    def _process(self, context):
        story_folder = os.path.join(config.server_root, config.stories_dir, context.id)
        
        # For each subfolder in the story_folder
        for subfolder in sorted(os.listdir(story_folder)):
            subfolder_path = os.path.join(story_folder, subfolder)
            
            # Check if the path is a directory and contains the required JSON file
            if os.path.isdir(subfolder_path) and '1_analysis_stage.json' in os.listdir(subfolder_path):
                
                scene_json_path = os.path.join(subfolder_path, 'scene.json')
                analysis_stage_json_path = os.path.join(subfolder_path, '1_analysis_stage.json')
                
                # Read the JSON file
                with open(scene_json_path, 'r') as scene_file, open(analysis_stage_json_path, 'r') as analysis_file:
                    scene_data = json.load(scene_file)
                    storycontent = scene_data.get('content', '')
                
                    analysis_data = json.load(analysis_file)
                    characters = analysis_data.get('characters', {})
                    
                    # Test data
                    # story_content = "WOLF, meeting with a Lamb astray from the fold, resolved not to lay violent hands on him, but to find some plea to justify to the Lamb the Wolf’s right to eat him. He thus addressed him: “Sirrah, last year you grossly insulted me.” “Indeed,” bleated the Lamb in a mournful tone of voice, “I was not then born.”"
                    # characters = "a wolf and a lamb"

                    llmOutput = llm.get_composition(story_content=storycontent, characters=json.dumps(characters))
                    character_composition_data = json.loads(llmOutput)

                    save_file_path = os.path.join(subfolder_path, '3_composition_stage.json')
                    if os.path.isfile(save_file_path):
                        os.remove(save_file_path)

                    # Save the aggregated data to a new JSON file in the current subfolder
                    with open(save_file_path, 'w') as output_file:
                        json.dump(character_composition_data, output_file, indent=4)

                    #############################
                    
                    # Hard coded version:
                    # character_composition_data = {"characters": {}}
                    # # For each character in the JSON
                    # for character_name, description in characters.items():
                    #     character_composition_data['characters'][character_name] = {
                    #         "distance_from_camera": 1,
                    #         "distance_from_the_center_in_degree": 0,
                    #         "distance_from_the_floor": 0,
                    #         "scale_x": 1,
                    #         "scale_y": 1,
                    #     }
                    # with open(os.path.join(subfolder_path, '3_test_composition_stage.json'), 'w') as output_file:
                    #     json.dump(character_composition_data, output_file, indent=4)

        return context