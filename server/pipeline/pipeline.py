import os
import json
from analyzerstage import AnalyzerStage
from segmentationstage import SegmentationStage
from charactergenstage import CharacterGenStage
from config import config

class Pipeline:
    def __init__(self):
        self.stages = [
            # SegmentationStage(),
            # AnalyzerStage(),
            CharacterGenStage()
        ]

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, context):
        # make job directory
        subfolder = os.path.join(config.server_root, config.stories_dir , context.id)
        os.makedirs(subfolder)
        story_path = os.path.join(config.server_root, config.stories_dir, context.id, 'story.json')

        with open(story_path, 'w') as f:
            json.dump({
                "id" : context.id,
                "title" : context.title,
                "story_data": context.story_data,
            }, f)

        for stage in self.stages:
            data = stage.process(context)
        return data