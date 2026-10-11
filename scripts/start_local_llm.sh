#!/usr/bin/env bash
# Serves a Hugging Face GGUF model on an OpenAI-compatible endpoint (http://localhost:1234/v1)
# so the examples run fully locally. Pair with OPENAI_BASE_URL / LLM_MODEL in .env.
#
#   scripts/start_local_llm.sh          # Qwen3.8-27B (default)
#   scripts/start_local_llm.sh gpt-oss  # gpt-oss-20b: faster, weaker Korean
set -euo pipefail

case "${1:-qwen}" in
  qwen)
    # Thinking is disabled because it multiplies latency on every agent step.
    exec llama-server -hf unsloth/Qwen3.8-27B-GGUF -hff Qwen3.8-27B-UD-Q4_K_XL.gguf \
      --jinja -c 32768 --host 127.0.0.1 --port 1234 \
      --chat-template-kwargs '{"enable_thinking":false}'
    ;;
  gpt-oss)
    # -hff is required: the repo also ships an eagle3 draft model that -hf would pick.
    exec llama-server -hf ggml-org/gpt-oss-20b-GGUF -hff gpt-oss-20b-MXFP4.gguf \
      --jinja -c 32768 --host 127.0.0.1 --port 1234
    ;;
  *)
    echo "usage: $0 [qwen|gpt-oss]" >&2
    exit 1
    ;;
esac
