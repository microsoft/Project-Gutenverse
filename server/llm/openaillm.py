import os
from config import config
import openai
import json

class OpenAiLLM:

    def __init__(self) -> None:
        openai.api_key = config.OpenAIApiKey
        self.segmentation_prompt = self._get_segmentation_prompt()
        self.analysis_prompt = self._get_analysis_prompt()

    def _get_segmentation_prompt(self):        
        file_path = os.path.join(config.server_root, "pipeline\\prompts\\segmentation_stage_prompt.txt")

        with open(file_path, 'r') as file:
            return file.read()
        
    def _get_analysis_prompt(self):
        file_path = os.path.join(config.server_root, "pipeline\\prompts\\analyzer_stage_prompt.txt")
        
        with open(file_path, 'r') as file:
            return file.read()
        
    def analize_scene(self, scene) -> str:
        analyzer_prompt = self.analysis_prompt.replace("{{story_data}}", scene.body)
        output = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo-16k",
                messages=[{
                    "role": "user",
                    "content": analyzer_prompt
                }]
            )
        print(output)
        return output["choices"][0]["message"]["content"]

    def segment_block_into_scenes(self, story_data: str) -> dict:
        prompt = self.segmentation_prompt.replace("{{story_data}}", story_data)
        output = self.prompt(prompt)
        jsonResponse = output["choices"][0]["message"]["content"]
        try:
            json_data = json.loads(jsonResponse)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
        json_data = json.loads(jsonResponse)
        return json_data

    def prompt(self, prompt: str):
        return openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

llm = OpenAiLLM()