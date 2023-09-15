from config import config
from PIL import Image
import openai
import requests

class DalleLLM:
    
    def __init__(self) -> None:
        openai.api_key = config.OpenAIApiKey

    def generate(self, prompt, negative_prompt = "", height = 512, width = 512):
        size = f"{height}x{width}"
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size,
            response_format="url"
        )

        url = response["data"][0]["url"]
        return Image.open(requests.get(url, stream=True).raw)