import openai
import dotenv
import os
import json
from stage import Stage

class AnalyzerStage(Stage):
    def process(self, context):
        dotenv.load_dotenv()
        openai.api_key = os.getenv ("OpenAIApiKey")

        output = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            messages=[{
                "role": "user",
                "content": self.create_analysis_prompt(context.story_data)
            }]
        )

        print(output)
        self.save_response_output(output["choices"][0]["message"]["content"], context)
        return output
    
    def save_response_output(self, response_payload, context):
        filename = "1_analysis_stage.json"
        file = os.path.join(context.filepath, filename)
        
        # Convert the string representation of JSON to a Python dictionary
        json_data = json.loads(response_payload)
        
        with open(file, "w") as f:
            json.dump(json_data, f, indent=4)


    
    def create_analysis_prompt(self, story_data):
        file_path = os.path.join(".\pipeline\prompts", "analyzer_stage_prompt.txt")
        
        with open(file_path, 'r') as file:
            content = file.read()
        
        analyzer_prompt = content.replace("{{story_data}}", story_data)
        
        return analyzer_prompt