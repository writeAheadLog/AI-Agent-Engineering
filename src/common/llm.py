"""Single switch point for the LLM and embedding models used by the examples.

Each example keeps its original OpenAI model as the default, so behaviour is
unchanged unless LLM_MODEL / EMBEDDING_MODEL / EMBEDDING_PROVIDER are set (e.g. to run against a
local OpenAI-compatible server via OPENAI_BASE_URL).
"""
import os

from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_HF_EMBEDDING_MODEL = "BAAI/bge-m3"


def resolve_model(default: str) -> str:
    return os.getenv("LLM_MODEL") or default


def get_chat_model(default: str, **kwargs) -> ChatOpenAI:
    # Non-reasoning OpenAI models reject reasoning_effort, so send it only on request.
    effort = os.getenv("LLM_REASONING_EFFORT")
    if effort:
        kwargs.setdefault("reasoning_effort", effort)
    return ChatOpenAI(model=resolve_model(default), **kwargs)


def get_embeddings() -> Embeddings:
    if os.getenv("EMBEDDING_PROVIDER") == "huggingface":
        # Imported lazily so the OpenAI path doesn't pay the torch import cost.
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name=os.getenv("EMBEDDING_MODEL") or DEFAULT_HF_EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},
        )
    # Local servers reject the token-id arrays sent when the context-length check is on.
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL,
        check_embedding_ctx_length=False,
    )
