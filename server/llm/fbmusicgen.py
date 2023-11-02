# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import time
import torch

from audiocraft.models import MusicGen
from config import config
from localllm import LocalLLM
from loguru import logger

class FbMusicGen(LocalLLM):
    def __repr__(self) -> str:
        return 'FbMusicGen'

    def __str__(self) -> str:
        return self.__repr__()

    def __init__(self):
        self.musicgen_model = None
        self.music_duration = 5    

    @property
    def sample_rate(self) -> int:
        return self.musicgen_model.sample_rate

    def _instantiate(self):
        start = time.time()
        # Load the Music Gen model with the CPU if we are not using the GPU, otherwise let Music Gen determine how to load the model
        self.musicgen_model = MusicGen.get_pretrained('facebook/musicgen-small', device="cpu" if not config.UseGpuAudioGen else None)
        end = time.time()
        logger.info(f"MusicGen Model took {end-start} seconds")
        self.musicgen_model.set_generation_params(duration=self.music_duration)
    
    def _dispose(self):
        del self.musicgen_model
        if config.UseGpuAudioGen:
            if torch.cuda.is_available():
                print(f'Clearing CUDA cache {self}')
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

    def set_music_duration(self, duration):
        self.music_duration = duration

    def generate(self, prompt):
        logger.info("MusicGen model about to generate...")
        start = time.time()
        wav = self.musicgen_model.generate([prompt])  # generates samples.
        end = time.time()
        logger.info(f"MusicGen Generation took {end-start} seconds")
        return wav