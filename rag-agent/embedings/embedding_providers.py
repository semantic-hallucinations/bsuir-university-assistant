from abc import ABC, abstractmethod
from typing import override

from fastembed import TextEmbedding
from ollama import Client

from .batched_texts import BatchedTexts


class EmbeddingProvider(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def encode(self, text: str) -> list[float]:
        """
        Embed a single text.
        Parameters:
            text: str
                The text to embed.
        Returns:
            list[float]
                The embedded text.
        """
        pass

    @abstractmethod
    def encode_batch(self, batch: list[str]) -> list[float]:
        """
        Embed batch of texts.
        Parameters:
            batch: list[str]
                A batch to encode
        Returns:
            list[float]
                Encoded values of batch.
        """
        pass

    def encode_documents(self, texts: list[str], batch_size: int) -> list[float]:
        """
        Embed many texts by batches.
        Parameters:
            texts: list[str]
                A list of documents to embed.
            batch_size: int
                Size of batch to use for encoding.
        Returns:
            list[str]
                A list of vectors for documents. Guaranteed that sequence of
            embeddings correspond to sequence of documents.
        """
        embeddings = []
        for batch in BatchedTexts(texts, batch_size):
            embeddings.extend(self.encode_batch(batch))
        return embeddings


def embed_factory(provider: str, model_name: str) -> EmbeddingProvider:
    if provider == "ollama":
        return OllamaEmbeddingProvider(model_name)
    elif provider == "fastembed":
        return FastEmbedProvider(model_name)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "bge-large"):
        super().__init__(model_name)
        self.ollama_client = Client()

    @override
    def encode(self, text: str) -> list[float]:
        return self.ollama_client.embed(text).embeddings[0]

    @override
    def encode_batch(self, batch):
        return self.ollama_client.embed(batch).embeddings

    def __str__(self):
        return f"OllamaEmbeddingProvider(model_name={self.model_name})"


class FastEmbedProvider(EmbeddingProvider):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.fastembed_model = TextEmbedding(model_name)

    @override
    def encode(self, text: str) -> list[float]:
        return next(self.fastembed_model.embed(text)).tolist()

    @override
    def encode_batch(self, batch):
        return list(self.fastembed_model.embed(batch))

    def __str__(self):
        return f"FastEmbedProvider(model_name={self.model_name})"
