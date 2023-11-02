# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import time
import torch

from audiocraft.models import AudioGen
from config import config
from localllm import LocalLLM
from loguru import logger

class FbAudioGen(LocalLLM):
    def __repr__(self) -> str:
        return 'FbAudioGen'

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self):
        self.audiogen_model = None
        self.audio_duration = 2
    
    @property
    def sample_rate(self) -> int:
        return self.audiogen_model.sample_rate

    def _instantiate(self):
        start = time.time()
        # Load the Audio Gen model with the CPU if we are not using the GPU, otherwise let Audio Gen determine how to load the model
        self.audiogen_model = AudioGen.get_pretrained('facebook/audiogen-medium', device="cpu" if not config.UseGpuAudioGen else None)
        end = time.time()
        logger.info(f"AudioGen Model took {end-start} seconds")
        self.audiogen_model.set_generation_params(duration=self.audio_duration)
    
    def _dispose(self):
        del self.audiogen_model
        if config.UseGpuAudioGen:
            if torch.cuda.is_available():
                print(f'Clearing CUDA cache {self}')
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

    def set_audio_duration(self, duration):
        self.audio_duration = duration
    
    def generate(self, prompt):
        logger.info("AudioGen model about to generate...")
        start = time.time()
        wav = self.audiogen_model.generate(prompt)  # generates samples.
        end = time.time()
        logger.info(f"AudioGen Generation took {end-start} seconds")
        return wav