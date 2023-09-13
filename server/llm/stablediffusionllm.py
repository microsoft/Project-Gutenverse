import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

class StableDiffusionLLM:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe = self.pipe.to("cuda")

    def __del__(self):
        del self.pipe
        if torch.cuda.is_available():
            print("Clearing CUDA cache")
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

    def generate(self, prompt, negative_prompt = "", height = 512, width = 512):
        result = self.pipe(prompt=prompt, negative_prompt=negative_prompt, height=height, width=width)
        image = result.images[0]
        return image