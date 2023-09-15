from stage import Stage
from config import config
from charactergen import CharacterGen
from skyboxgen import SkyboxGen

from llm import *

class ImageGenStage(Stage):
    def __repr__(self) -> str:
        return 'ImageGenStage'

    def __str__(self) -> str:
        return self.__repr__()
    
    def _initialize(self):
        if config.UseGpuImageGen:
            self.imageGenLLM = KandinskyLLM()
            self.imageGenLLM.instantiate()
        else:
            self.imageGenLLM = DalleLLM()
        
        self.characterGen = CharacterGen()
        self.skyboxGen = SkyboxGen()

    def _dispose(self):
        del self.characterGen
        del self.skyboxGen

        if config.UseGpuImageGen:
            self.imageGenLLM.dispose()
    
    def _process(self, context):
        context = self.characterGen.process(context, self.imageGenLLM)
        context = self.skyboxGen.process(context, self.imageGenLLM)
        return context
