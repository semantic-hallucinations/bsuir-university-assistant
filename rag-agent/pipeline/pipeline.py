from llama_index.core.indices.base import BaseIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import PromptTemplate
from fastapi import Depends

from .dependencies import get_index


qa_prompt = PromptTemplate(
    "Answer ONLY in English and ONLY using the data provided.\n"
    "Answer format:\n"
    "1. [item]\n"
    " - [Item details]\n"
    "2. [Next item]\n"
    "Use only data from these sections:\n{context_str}\n\n"
    "Question: {query_str}\n"
    "Answer:"
)


def create_ingestion_pipeline():
    return IngestionPipeline(
        transformations=[
        ]
    )


def setup_rag_pipeline(
    index: BaseIndex = Depends(get_index)
):

    return index.as_query_engine(
        text_qa_template=qa_prompt,
        similarity_top_k=7,
        response_mode="compact"
    )
