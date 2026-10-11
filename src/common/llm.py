"""Single switch point for the LLM and embedding models used by the examples.

Each example keeps its original OpenAI model as the default, so behaviour is
unchanged unless LLM_MODEL / EMBEDDING_MODEL are set.
"""
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"


def resolve_model(default: str) -> str:
    return os.getenv("LLM_MODEL") or default


def get_chat_model(default: str, **kwargs) -> ChatOpenAI:
    # Non-reasoning OpenAI models reject reasoning_effort, so send it only on request.
    effort = os.getenv("LLM_REASONING_EFFORT")
    if effort:
        kwargs.setdefault("reasoning_effort", effort)
    return ChatOpenAI(model=resolve_model(default), **kwargs)


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL)
