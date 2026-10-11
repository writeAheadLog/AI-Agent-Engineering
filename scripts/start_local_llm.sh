#!/usr/bin/env bash
# Serves a Hugging Face GGUF model on an OpenAI-compatible endpoint (http://localhost:1234/v1)
# so the examples run fully locally. Pair with OPENAI_BASE_URL / LLM_MODEL in .env.
#
#   scripts/start_local_llm.sh                          # Qwen3.8-27B (default preset)
#   scripts/start_local_llm.sh gpt-oss                  # gpt-oss-20b preset: faster, weaker Korean
#   scripts/start_local_llm.sh <hf-repo>[:quant] [file.gguf] [llama-server args...]
#       e.g. scripts/start_local_llm.sh unsloth/gemma-4-26b-a4b-it-GGUF:Q4_K_M
#   scripts/start_local_llm.sh --download [preset | <hf-repo>[:quant] [file.gguf]]
#       Downloads the LLM plus the embedding models into ~/.cache/huggingface without serving.
#
# Env: LLM_PORT (default 1234; keep OPENAI_BASE_URL in sync), LLM_CTX (default 32768),
#      EMBEDDING_MODEL (default BAAI/bge-m3; used by --download).
set -euo pipefail

cd "$(dirname "$0")/.."

PORT="${LLM_PORT:-1234}"
CTX="${LLM_CTX:-32768}"
# ch09 metrics load all-MiniLM-L6-v2 directly, so it is fetched alongside the configured model.
EMBEDDING_MODELS=("${EMBEDDING_MODEL:-BAAI/bge-m3}" "sentence-transformers/all-MiniLM-L6-v2")

usage() {
  sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
}

MODE=serve
if [[ "${1:-}" == "--download" ]]; then
  MODE=download
  shift
fi

SPEC="${1:-qwen}"
EXTRA=()
case "$SPEC" in
  qwen)
    REPO=unsloth/Qwen3.8-27B-GGUF
    FILE=Qwen3.8-27B-UD-Q4_K_XL.gguf
    # Thinking is disabled because it multiplies latency on every agent step.
    EXTRA=(--chat-template-kwargs '{"enable_thinking":false}')
    ;;
  gpt-oss)
    # The file is pinned: the repo also ships an eagle3 draft model that -hf would pick.
    REPO=ggml-org/gpt-oss-20b-GGUF
    FILE=gpt-oss-20b-MXFP4.gguf
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  */*)
    REPO=$1
    shift
    FILE=""
    if [[ "${1:-}" == *.gguf ]]; then
      FILE=$1
      shift
    fi
    EXTRA=("$@")
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac

download() {
  local repo=${REPO%%:*} quant=""
  [[ "$REPO" == *:* ]] && quant=${REPO#*:}
  if [[ -n "$FILE" ]]; then
    uv run hf download "$repo" "$FILE"
  elif [[ -n "$quant" ]]; then
    uv run hf download "$repo" --include "*${quant}*.gguf"
  else
    echo "다운로드할 파일(file.gguf) 또는 양자화(<repo>:Q4_K_M)를 지정하세요. 저장소 전체는 받지 않습니다." >&2
    exit 1
  fi
  for model in "${EMBEDDING_MODELS[@]}"; do
    uv run python -c "import sys; from sentence_transformers import SentenceTransformer; SentenceTransformer(sys.argv[1])" "$model"
  done
  echo "다운로드 완료. 서버 실행: scripts/start_local_llm.sh $SPEC"
}

# --jinja applies the model's own chat template, which tool calling depends on.
serve() {
  exec llama-server -hf "$REPO" ${FILE:+-hff "$FILE"} \
    --jinja -c "$CTX" --host 127.0.0.1 --port "$PORT" ${EXTRA[@]+"${EXTRA[@]}"}
}

if [[ "$MODE" == download ]]; then
  download
else
  serve
fi
