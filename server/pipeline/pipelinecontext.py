import uuid
from dataclasses import dataclass, field


@dataclass
class Scene:
    name: str
    body: str
    start_index: int
    end_index: int
    index: int

@dataclass
class SegmentationAnalysis:
    scenes: list[Scene] = field(default_factory=list)
    last_processed_index: int = 0

@dataclass
class PipelineContext:
    title: str = ''
    id: str = '9bac39d6-faa3-41ac-8b7a-b920a58464f8' #str(uuid.uuid4())
    story_data: str  = ''
    segmentation_analysis: SegmentationAnalysis = field(default_factory=SegmentationAnalysis)

@dataclass
class CheckpointData:
    context: PipelineContext
    end: int
    completed: bool
