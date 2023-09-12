import uuid
from dataclasses import dataclass

@dataclass
class PipelineContext:
    title: str = ''
    id: str = str(uuid.uuid4())
    story_data: str  = ''
    segmentation_analysis: object = object() # placeholder for segmentation stage