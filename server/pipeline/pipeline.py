import os
import json
from analyzerstage import AnalyzerStage
from segmentationstage import SegmentationStage
from stage import Stage
from config import config

class Pipeline:
    def __init__(self):
        self.stages = [
            SegmentationStage(),
            AnalyzerStage()
        ]

    def _teardown_all_stage_checkpoints(self):
        def apply_teardown(stage: Stage):
            stage._teardown_checkpoints()
        map(apply_teardown, self.stages)

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, context):
        # make job directory
        subfolder = os.path.join(config.server_root, config.stories_dir , context.id)
        os.makedirs(subfolder,exist_ok=True)
        story_path = os.path.join(config.server_root, config.stories_dir, context.id, 'story.json')

        with open(story_path, 'w') as f:
            json.dump({
                "id" : context.id,
                "title" : context.title,
                "story_data": context.story_data,
            }, f)

        for stage in self.stages:
            context = stage.process(context)
        # self._teardown_all_stage_checkpoints()
        return