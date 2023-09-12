import openai
import dotenv
import os
import json
from stage import Stage
from config import config
from llm import llm

class AnalyzerStage(Stage):
    def process(self, context):
        for i, scene in enumerate(context.segmentation_analysis.scenes):
            analyis = llm.analize_scene(scene)
            try:
                self.save_response_output(analyis, context, i)
                print("Successfully produced analysis for scene " + str(i))
            except:
                print("Encountered an error processing story " + str(i) + " skipping this story")
    
    def save_response_output(self, response_payload, context, sceneIndex):
        filename = "1_analysis_stage.json"
        scene_dir = os.path.join(config.server_root, config.stories_dir, context.id, str(sceneIndex))
        file = os.path.join(scene_dir, filename)

        # Convert the string representation of JSON to a Python dictionary
        json_data = json.loads(response_payload)
        
        with open(file, "w") as f:
            json.dump(json_data, f, indent=4)

