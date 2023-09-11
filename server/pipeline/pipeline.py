import os
from analyzerstage import AnalyzerStage
from segmentationstage import SegmentationStage

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
        subfolder = os.path.join(os.path.abspath(".") + "\\stories", context.id)
        os.makedirs(subfolder)
        context.filepath = os.path.abspath(subfolder)

        for stage in self.stages:
            data = stage.process(context)
        return data