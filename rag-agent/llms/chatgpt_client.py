from typing import override

from openai import OpenAI

from .llm_client import LLMClient


class ChatGPTClient(LLMClient):
    def __init__(
        self,
        token: str,
        model_name: str = "gpt-4",
        system_prompt: str = "You are an unbiased and helpful bot, you never lie or make things up",
        include_metadata: bool = False,
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.include_metadata = include_metadata
        self.client = OpenAI(api_key=token)

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
