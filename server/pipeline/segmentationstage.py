import json
import os
from dataclasses import dataclass, field
from stage import Stage
from config import config
from llm import llm

@dataclass
class Scene:
    title: str
    content: str
    start_index: str
    end_index: str

@dataclass
class SegmentationAnalysis:
    scenes: list = field(default_factory=list)
    last_processed_index: int = 0

class SegmentationStage(Stage):
    def __init__(self, segment_only_once=True):
        self.segment_only_once = segment_only_once

    def process(self, context):
        analysis = SegmentationAnalysis()
        start_index = 0
        if self.segment_only_once:
            end_index = min(start_index + 25000, len(context.story_data))
            block = context.story_data[start_index:end_index]
            self._segment_block_into_scenes(block, analysis)
        else:
            while start_index < len(context.story_data):
                end_index = min(start_index + 25000, len(context.story_data))
                block = context.story_data[start_index:end_index]
                self._segment_block_into_scenes(block, analysis)

                if (analysis.last_processed_index != end_index and end_index < len(context.story_data)):
                    end_index = analysis.last_processed_index

                start_index = end_index

        # Save scenes to JSON files
        for i, scene in enumerate(analysis.scenes):
            scene_folder = os.path.join(config.server_root, config.stories_dir, context.id, str(i))
            os.makedirs(scene_folder, exist_ok=True)
            with open(os.path.join(scene_folder, 'scene.json'), 'w') as f:
                json.dump({
                    "title": scene["name"],
                    "content": scene["body"],
                    "start_index": scene["startIndex"],
                    "end_index": scene["endIndex"]
                }, f)
        context.segmentation_analysis = analysis

    def _segment_block_into_scenes(self, block: str, analysis: SegmentationAnalysis):

        json_data = llm.segment_block_into_scenes(block)
        analysis.last_processed_index = json_data["endIndex"]
        for scene in json_data["scenes"]:
            analysis.scenes.append(scene)
