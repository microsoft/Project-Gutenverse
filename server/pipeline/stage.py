import os
from config import config
from loguru import logger
from abc import ABC, abstractmethod

from pipelinecontext import PipelineContext

class Stage(ABC):
    def process(self, context):
        logger.debug(f'Processing stage: {__class__}')
        context = self._load_checkpoint(context)
        return self._process(context)


    @abstractmethod
    def _process(self, context):
        # Process the data
        raise NotImplementedError
    
    def _checkpoint_path(self, context):
        return os.path.join(config.server_root, config.stories_dir, context.id, f'{self}_checkpoint.json')

    def _checkpoint(self, *args, **kwargs) -> bool:
        # Should be overridden to give checkpointing
        pass
    

    def _load_checkpoint(self, context: PipelineContext) -> PipelineContext:
        # Should be overridden to give checkpointing
        return context

    def _teardown_checkpoints(self, context):
        checkpoint_path = self._checkpoint_path(context)
        # Check if file exists then delete it
        if os.path.isfile(checkpoint_path):
            os.remove(checkpoint_path)
        else:
           logger.error(f"{checkpoint_path} does not exist for removing checkpoint")
            
