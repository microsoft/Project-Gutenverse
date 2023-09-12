import uuid

class PipelineContext:
    def __init__(self):
        self.title = ''
        self.id = str(uuid.uuid4())
        self.story_data = ''
        self.filepath = ''
        self.segmentation_analysis = object() # placeholder for segmentation stage