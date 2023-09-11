import json
import os
import dotenv
import openai
from stage import Stage

class Scene:
    def __init__(self, title, content, start_index, end_index):
        self.title = title
        self.content = content
        self.start_index = start_index
        self.end_index = end_index

class SegmentationAnalysis:
    def __init__(self):
        self.scenes = []
        self.last_processed_index = 0

class SegmentationStage(Stage):
    def __init__(self):
        pass

    def process(self, context):
        analysis = SegmentationAnalysis()
        start_index = 0
        while start_index < len(context.story_data):
            end_index = min(start_index + 25000, len(context.story_data))
            block = context.story_data[start_index:end_index]
            self._segment_block_into_scenes(block, analysis)

            if (analysis.last_processed_index != end_index and end_index < len(context.story_data)):
                end_index = analysis.last_processed_index

            start_index = end_index

        # Save scenes to JSON files
        for i, scene in enumerate(analysis.scenes):
            scene_folder = os.path.join(context.filepath, str(i))
            os.makedirs(scene_folder, exist_ok=True)
            with open(os.path.join(scene_folder, 'scene.json'), 'w') as f:
                json.dump({
                    "title": scene["name"],
                    "content": scene["body"],
                    "start_index": scene["startIndex"],
                    "end_index": scene["endIndex"]
                }, f)

    def _segment_block_into_scenes(self, block, analysis):
        dotenv.load_dotenv()
        openai.api_key = os.getenv ("OpenAIApiKey")

        output = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            messages=[{
                "role": "user",
                "content": self.create_segmentation_prompt(block)
            }]
        )

        jsonResponse = output["choices"][0]["message"]["content"]
        print(jsonResponse)
        json_data = json.loads(jsonResponse)
        analysis.last_processed_index = json_data["endIndex"]
        for i, scene in enumerate(json_data["scenes"]):
            analysis.scenes.append(scene)

    def create_segmentation_prompt(self, story_data):
        file_path = os.path.join(".\pipeline\prompts", "segmentation_stage_prompt.txt")
        
        with open(file_path, 'r') as file:
            content = file.read()
        
        segmentation_prompt = content.replace("{{story_data}}", story_data)
        
        return segmentation_prompt