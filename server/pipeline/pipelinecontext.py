import uuid
from dataclasses import dataclass, field
from utilities import story_title_to_hash
from typing import List

@dataclass
class Scene:
    name: str
    body: str
    start_index: int
    end_index: int
    index: int

@dataclass
class SegmentationAnalysis:
    # scenes: list[Scene] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list)
    last_processed_index: int = 0

@dataclass
class PipelineContext:
    title: str = ''
    story_data: str  = ''
    segmentation_analysis: SegmentationAnalysis = field(default_factory=SegmentationAnalysis)
    _id: str = ''

    @property
    def id(self):
        if not self._id:
            id_ = story_title_to_hash(self.title)
            self._id = id_
        return self._id

@dataclass
class CheckpointData:
    context: PipelineContext
    end: int
    completed: bool
