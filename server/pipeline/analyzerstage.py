import openai
import dotenv
import os
import json
import uuid
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
        subfolder = os.path.join("../stories", context.id)
        os.makedirs(subfolder)

        filename = "1_analysis_stage.json"
        file = os.path.join(subfolder, filename)
        
        # Convert the string representation of JSON to a Python dictionary
        json_data = json.loads(response_payload)
        
        with open(file, "w") as f:
            json.dump(json_data, f, indent=4)


    
    def create_analysis_prompt(self, story_data):
        file_path = os.path.join("prompts", "analyzer_stage_prompt.txt")
        
        with open(file_path, 'r') as file:
            content = file.read()
        
        analyzer_prompt = content.replace("{{story_data}}", story_data)
        
        return analyzer_prompt

from pipelinecontext import PipelineContext
testData = PipelineContext()
testData.story_data = '''
The Hare and the Tortoise

A HARE one day ridiculed the short feet and slow pace of the Tortoise,
who replied, laughing: “Though you be swift as the wind, I will beat you
in a race.” The Hare, believing her assertion to be simply impossible,
assented to the proposal; and they agreed that the Fox should choose
the course and fix the goal. On the day appointed for the race the two
started together. The Tortoise never for a moment stopped, but went on
with a slow but steady pace straight to the end of the course. The Hare,
lying down by the wayside, fell fast asleep. At last waking up, and
moving as fast as he could, he saw the Tortoise had reached the goal,
and was comfortably dozing after her fatigue.

Slow but steady wins the race.'''

stage = AnalyzerStage()
stage.process(testData)