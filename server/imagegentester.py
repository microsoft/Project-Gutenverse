from llm import KandinskyLLM

pipeline = KandinskyLLM()
while (True):
    prompt = input("Enter a prompt: ")
    negative_prompt = input("Enter a negative prompt: ")
    image = pipeline.generate(prompt=prompt, negative_prompt=negative_prompt)
    image.save(prompt + ".png")