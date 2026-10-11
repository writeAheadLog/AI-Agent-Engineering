#!/usr/bin/env bash
# Serves a Hugging Face GGUF model on an OpenAI-compatible endpoint (http://localhost:1234/v1)
# so the examples run fully locally. Pair with OPENAI_BASE_URL / LLM_MODEL in .env.
#
#   scripts/start_local_llm.sh                          # Qwen3.8-27B (default preset)
#   scripts/start_local_llm.sh gpt-oss                  # gpt-oss-20b preset: faster, weaker Korean
#   scripts/start_local_llm.sh <hf-repo>[:quant] [file.gguf] [llama-server args...]
#       e.g. scripts/start_local_llm.sh unsloth/gemma-4-26b-a4b-it-GGUF:Q4_K_M
#
# Env: LLM_PORT (default 1234; keep OPENAI_BASE_URL in sync), LLM_CTX (default 32768).
set -euo pipefail

PORT="${LLM_PORT:-1234}"
CTX="${LLM_CTX:-32768}"

usage() {
  sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
}

# --jinja applies the model's own chat template, which tool calling depends on.
serve() {
  local repo=$1 file=$2
  shift 2
  exec llama-server -hf "$repo" ${file:+-hff "$file"} \
    --jinja -c "$CTX" --host 127.0.0.1 --port "$PORT" "$@"
}

case "${1:-qwen}" in
  qwen)
    # Thinking is disabled because it multiplies latency on every agent step.
    serve unsloth/Qwen3.8-27B-GGUF Qwen3.8-27B-UD-Q4_K_XL.gguf \
      --chat-template-kwargs '{"enable_thinking":false}'
    ;;
  gpt-oss)
    # The file is pinned: the repo also ships an eagle3 draft model that -hf would pick.
    serve ggml-org/gpt-oss-20b-GGUF gpt-oss-20b-MXFP4.gguf
    ;;
  -h|--help)
    usage
    ;;
  */*)
    repo=$1
    shift
    file=""
    if [[ "${1:-}" == *.gguf ]]; then
      file=$1
      shift
    fi
    serve "$repo" "$file" "$@"
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
