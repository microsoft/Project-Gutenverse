# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import json
import os
from dataclasses import dataclass
from loguru import logger
from stage import Stage
from config import config
from llm import llm
from pipelinecontext import *
from utilities import dataclass_to_dict
from dacite import from_dict


class SegmentationStage(Stage):

    def __repr__(self) -> str:
        return 'SegmentationStage'

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self, segment_only_once=True):
        self.segment_only_once = segment_only_once
        

    def _checkpoint(self, *args, context, end, completed=False, **kwargs) -> bool:
        checkpoint = CheckpointData(context, end, completed)
        with open(self._checkpoint_path(context), 'w') as f:
            f.write(json.dumps(dataclass_to_dict(checkpoint)))
        return True
    
    def _load_checkpoint(self, context: PipelineContext) -> PipelineContext:
        checkpoint_path = self._checkpoint_path(context)
        if not os.path.isfile(checkpoint_path):
            return context

        logger.debug(f'Checkpoint found for stage: {self.__class__}')
        with open(checkpoint_path, 'r') as f:
            checkpoint_data = from_dict(data=json.loads(f.read()), data_class=CheckpointData)

        if checkpoint_data.completed:
            checkpoint_data.context.story_data = ''
        else:
            context.story_data = checkpoint_data.context.story_data[checkpoint_data.end:]
        
        return checkpoint_data.context
    
    def _process(self, context: PipelineContext):
        if len(context.story_data) == 0:
            return context
        analysis = context.segmentation_analysis
        start_index = 0
        if self.segment_only_once :
            end_index = min(start_index + 25000, len(context.story_data))
            block = context.story_data[start_index:end_index]
            self._segment_block_into_scenes(block, analysis)
            self._checkpoint(context=context, end=end_index)
        else:
            while start_index < len(context.story_data):
                end_index = min(start_index + 25000, len(context.story_data))
                block = context.story_data[start_index:end_index]
                self._segment_block_into_scenes(block, analysis)

                if (analysis.last_processed_index != end_index and end_index < len(context.story_data)):
                    end_index = analysis.last_processed_index

                start_index = end_index
                self._checkpoint(context=context, end=end_index)

        logger.info(f"{len(analysis.scenes)} scenes found")
        # Save scenes to JSON files
        for scene in analysis.scenes:
            scene_folder = os.path.join(config.server_root, config.stories_dir, context.id, str(scene.index))
            os.makedirs(scene_folder, exist_ok=True)
            with open(os.path.join(scene_folder, 'scene.json'), 'w') as f:
                json.dump({
                    "title": scene.name,
                    "content": scene.body,
                    "start_index": scene.start_index,
                    "end_index": scene.end_index
                }, f)
        self._checkpoint(context=context, end=end_index, completed=True)
        return context

    def _segment_block_into_scenes(self, block: str, analysis: SegmentationAnalysis):

        json_data = llm.segment_block_into_scenes(block)
        analysis.last_processed_index = json_data["end_index"]
        number_of_previous_scenes = len(analysis.scenes)
        for local_index, scene in enumerate(json_data["scenes"]):
            analysis.scenes.append(Scene(**scene, index=local_index+number_of_previous_scenes))
