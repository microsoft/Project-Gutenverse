import openai
import dotenv
import os
import json
from stage import Stage
from config import config

class AnalyzerStage(Stage):
    def process(self, context):
        dotenv.load_dotenv()
        openai.api_key = os.getenv ("OpenAIApiKey")

        for i, scene in enumerate(context.segmentation_analysis.scenes):
            output = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo-16k",
                messages=[{
                    "role": "user",
                    "content": self.create_analysis_prompt(scene["body"])
                }]
            )

            print(output)
            try:
                self.save_response_output(output["choices"][0]["message"]["content"], context, i)
                print("Successfully produced analysis for scene " + str(i))
            except:
                print("Encountered an error processing story " + str(i) + " skipping this story")
                

        return output
    
    def save_response_output(self, response_payload, context, sceneIndex):
        filename = "1_analysis_stage.json"
        scene_dir = os.path.join(config.server_root, config.stories_dir, context.id, str(sceneIndex))
        file = os.path.join(scene_dir, filename)

        # Convert the string representation of JSON to a Python dictionary
        json_data = json.loads(response_payload)
        
        with open(file, "w") as f:
            json.dump(json_data, f, indent=4)

    def create_analysis_prompt(self, story_data):
        file_path = os.path.join(".\server\pipeline\prompts", "analyzer_stage_prompt.txt")
        
        with open(file_path, 'r') as file:
            content = file.read()
        
        analyzer_prompt = content.replace("{{story_data}}", story_data)
        
        return analyzer_prompt