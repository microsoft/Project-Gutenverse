class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, data):
        for stage in self.stages:
            data = stage.process(data)
        return data

class Stage:
    def process(self, data):
        # Process the data
        pass

class TextProcessingStage(Stage):
    def process(self, data):
        # Specific text processing logic
        return modified_data