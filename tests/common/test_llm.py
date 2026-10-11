import pytest

from src.common.llm import get_chat_model, get_embeddings, resolve_model


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    for var in ("LLM_MODEL", "LLM_REASONING_EFFORT", "EMBEDDING_MODEL", "EMBEDDING_PROVIDER"):
        monkeypatch.delenv(var, raising=False)


def test_resolve_model_keeps_caller_default_when_env_unset():
    assert resolve_model("gpt-4o") == "gpt-4o"


def test_resolve_model_prefers_env_override(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-oss-20b")
    assert resolve_model("gpt-4o") == "openai/gpt-oss-20b"


def test_chat_model_uses_resolved_model_and_passes_kwargs(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-oss-20b")
    llm = get_chat_model("gpt-4o", temperature=0.0)
    assert llm.model_name == "openai/gpt-oss-20b"
    assert llm.temperature == 0.0


def test_chat_model_sends_reasoning_effort_only_when_configured(monkeypatch):
    assert get_chat_model("gpt-4o").reasoning_effort is None
    monkeypatch.setenv("LLM_REASONING_EFFORT", "low")
    assert get_chat_model("gpt-4o").reasoning_effort == "low"


def test_embeddings_model_is_configurable(monkeypatch):
    assert get_embeddings().model == "text-embedding-ada-002"
    monkeypatch.setenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
    assert get_embeddings().model == "text-embedding-nomic-embed-text-v1.5"


def test_huggingface_embeddings_run_locally(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "huggingface")
    monkeypatch.setenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    embeddings = get_embeddings()
    near, far = embeddings.embed_documents(["low inventory", "weather is nice"])
    query = embeddings.embed_query("stock shortage")
    assert sum(q * n for q, n in zip(query, near)) > sum(q * f for q, f in zip(query, far))
