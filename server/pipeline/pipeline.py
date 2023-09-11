class Pipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, data):
        for stage in self.stages:
            data = stage.process(data)
        return data