# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from config import config
from PIL import Image
import openai
import requests
from openai import OpenAI


class DalleLLM:
    
    def __init__(self) -> None:
        openai.api_key = config.OpenAIApiKey

    def generate(self, prompt, negative_prompt = "", height = 512, width = 512):
        client = OpenAI(api_key=config.OpenAIApiKey)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # response = openai.Image.create(
        #     prompt=prompt,
        #     n=1,
        #     size=size,
        #     response_format="url"
        # )

        url = response.data[0].url
        return Image.open(requests.get(url, stream=True).raw)