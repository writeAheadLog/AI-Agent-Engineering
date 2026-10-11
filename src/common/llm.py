"""Single switch point for the LLM and embedding models used by the examples.

Each example keeps its original OpenAI model as the default, so behaviour is
unchanged unless LLM_MODEL / EMBEDDING_MODEL / EMBEDDING_PROVIDER are set (e.g. to run against a
local OpenAI-compatible server via OPENAI_BASE_URL).
"""
import os
import socket
from urllib.parse import urlparse

from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_HF_EMBEDDING_MODEL = "BAAI/bge-m3"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


class LocalLLMServerUnavailable(RuntimeError):
    pass


def _ensure_local_server_reachable(base_url: str) -> None:
    # Fail at model creation with setup guidance instead of a bare "Connection refused"
    # on the first LLM call. A raw socket keeps this usable inside Temporal's sandbox,
    # which restricts urllib.request.
    url = urlparse(base_url)
    if url.hostname not in LOCAL_HOSTS:
        return
    try:
        socket.create_connection((url.hostname, url.port or 80), timeout=2).close()
    except OSError as e:
        raise LocalLLMServerUnavailable(
            f"로컬 LLM 서버({base_url})에 연결할 수 없습니다.\n"
            "  - 로컬 모델 사용: 다른 터미널에서 scripts/start_local_llm.sh 를 실행하세요.\n"
            "  - OpenAI API 사용: .env에서 OPENAI_BASE_URL을 지우고 OPENAI_API_KEY를 설정하세요.\n"
            "  자세한 내용은 README.md의 '환경 설정' 5단계를 참고하세요."
        ) from e


def resolve_model(default: str) -> str:
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        _ensure_local_server_reachable(base_url)
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
