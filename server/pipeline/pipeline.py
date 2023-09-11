import os
from analyzerstage import AnalyzerStage

class Pipeline:
    def __init__(self):
        self.stages = [
            AnalyzerStage()
        ]

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, context):
        # make job directory
        subfolder = os.path.join("../stories", context.id)
        os.makedirs(subfolder)
        context.filepath = subfolder

        for stage in self.stages:
            data = stage.process(context)
        return data