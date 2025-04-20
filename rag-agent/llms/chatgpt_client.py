from typing import override

from openai import OpenAI

from .llm_client import LLMClient
from ..settings import settings


class ChatGPTClient(LLMClient):
    def __init__(
        self,
        token: str = settings.get_model_key(),
        model_name: str = settings.get_model_name(),
        system_prompt: str = "You are an unbiased and helpful bot, you never lie or make things up",
        include_metadata: bool = False,
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.include_metadata = include_metadata
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=token)

    @override
    def chat(self, prompt):

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
        )

        if self.include_metadata:
            return response
        else:
            return response.choices[0].message.content
