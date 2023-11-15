# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
import openai

from openai import OpenAI
import json

from config import config

class OpenAiLLM:

    def __init__(self) -> None:
        openai.api_key = config.OpenAIApiKey
        self.segmentation_prompt = self._get_segmentation_prompt()
        self.analysis_prompt = self._get_analysis_prompt()
        self.compositon_prompt = self._get_composition_prompt()

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

        client = OpenAI(api_key=config.OpenAIApiKey)
        output = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "user", "content": analyzer_prompt},
        ])

        print(output)
        return output.choices[0].message.content

    def segment_block_into_scenes(self, story_data: str) -> dict:
        prompt = self.segmentation_prompt.replace("{{story_data}}", story_data)
        output = self.prompt(prompt)
        jsonResponse = output.choices[0].message.content
        if (jsonResponse.startswith('json')):
            jsonResponse = jsonResponse.strip('json')
        try:
            json_data = json.loads(jsonResponse)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
        json_data = json.loads(jsonResponse)
        return json_data

    def _get_composition_prompt(self):
        file_path = os.path.join(config.server_root, "pipeline\\prompts\\composition_stage_prompt.txt")
        
        with open(file_path, 'r') as file:
            return file.read()
        
    def get_composition(self, story_content, characters) -> str:
        composition_prompt = self.compositon_prompt.replace("{{story_content}}", story_content)
        composition_prompt = self.compositon_prompt.replace("{{characters}}", characters)
        
        client = OpenAI(api_key=config.OpenAIApiKey)
        output = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "user", "content": composition_prompt},
        ])
        print(output)
        return output.choices[0].message.content
    
    def prompt(self, prompt: str):
        client = OpenAI(api_key=config.OpenAIApiKey)
        output = client.chat.completions.create(
            response_format={ "type": "json_object" },
            model="gpt-4-1106-preview",
    
            messages=[
                {"role": "user", "content": prompt},
            ])
        return output

llm = OpenAiLLM()