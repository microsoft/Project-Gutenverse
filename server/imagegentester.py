from llm import *

pipeline = KandinskyLLM()
while (True):
    prompt = input("Enter a prompt: ")
    negative_prompt = input("Enter a negative prompt: ")
    image = pipeline.generate(prompt=prompt, negative_prompt=negative_prompt, height=512, width=512)
    image.save(prompt + ".png")