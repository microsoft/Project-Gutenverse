from llm import *
from transparent_background import Remover

pipeline = KandinskyLLM()
pipeline.instantiate()
remover = Remover()
while (True):
    prompt = input("Enter a prompt: ")
    negative_prompt = input("Enter a negative prompt: ")
    image = pipeline.generate(prompt=prompt, negative_prompt=negative_prompt, height=512, width=512)
    image_bg_removed = Image.fromarray(remover.process(image))
    image_bg_removed.save(prompt + ".png")
