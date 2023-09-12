import os
import json
from pipeline.analyzerstage import AnalyzerStage
from pipeline.segmentationstage import SegmentationStage
from config import config

class Pipeline:
    def __init__(self):
        self.stages = [
            SegmentationStage(),
            AnalyzerStage()
        ]

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, context):
        # make job directory
        subfolder = os.path.join(os.path.abspath("."), config.stories_dir , context.id)
        os.makedirs(subfolder)
        context.filepath = subfolder
        with open(os.path.join(context.filepath, 'story.json'), 'w') as f:
            json.dump({
                "id" : context.id,
                "title" : context.title,
                "story_data": context.story_data,
            }, f)

        for stage in self.stages:
            data = stage.process(context)
        return data