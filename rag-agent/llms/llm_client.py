from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def chat(self, prompt: str):
        """Response to a query"""
