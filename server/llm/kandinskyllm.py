import torch

from diffusers import AutoPipelineForText2Image
from localllm import LocalLLM

class KandinskyLLM(LocalLLM):
    
    def __repr__(self) -> str:
        return 'KandinskyLLM'

    def __str__(self) -> str:
        return self.__repr__()

    def _instantiate(self):
        self.pipe = AutoPipelineForText2Image.from_pretrained("kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16)
        self.pipe = self.pipe.to("cuda")

    def _dispose(self):
        del self.pipe
        if torch.cuda.is_available():
            print(f'Clearing CUDA cache {self}')
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

    def generate(self, prompt, negative_prompt = "", prior_guidance_scale = 1.0, height = 512, width = 512):
        result = self.pipe(prompt=prompt, negative_prompt=negative_prompt, prior_guidance_scale=prior_guidance_scale, height=height, width=width)
        image = result.images[0]
        return image