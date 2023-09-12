from diffusers import AutoPipelineForText2Image
import torch

class KandinskyLLM:
    def __init__(self):
        self.pipe = AutoPipelineForText2Image.from_pretrained("kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16)
        self.pipe = self.pipe.to("cuda")

    def generate(self, prompt, negative_prompt = "", prior_guidance_scale = 1.0, height = 768, width = 768):
        result = self.pipe(prompt=prompt, negative_prompt=negative_prompt, prior_guidance_scale=prior_guidance_scale, height=height, width=width)
        image = result.images[0]
        return image