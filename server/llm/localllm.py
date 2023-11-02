# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from abc import ABC, abstractmethod
from loguru import logger

class LocalLLM(ABC):
    
    def instantiate(self):
        logger.debug(f'Instantiate {self}')
        self._instantiate()

    def dispose(self):
        logger.debug(f'Dispose {self}')
        self._dispose()
    
    @abstractmethod
    def _instantiate(self):
        raise NotImplementedError
    
    @abstractmethod
    def _dispose(self):
        raise NotImplementedError
    
    