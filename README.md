# AI 에이전트 엔지니어링

<img src=cover.png width=300px>

한빛미디어에서 출간된 \[AI 에이전트 엔지니어링](원제: Building Applications with AI Agents)의 예시 코드 저장소입니다.

구매 링크
- 교보문고: https://product.kyobobook.co.kr/detail/S000219002818
- Yes24: https://www.yes24.com/product/goods/174018513
- 알라딘: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=384025599&start=pbook
- 리디: https://ridibooks.com/books/6071001294

## 예시 코드

이 책의 예제 코드는 깃허브에서 다운로드 할 수 있습니다. 한국어판 예제 코드는 업데이트를 반영하여 Python 3.12와 LangChain 1.0 환경에 맞게 수정하고, 장별로 정리했습니다. 예제에서 사용하는 일부 의존성의 특성상 윈도에서는 WSL 환경에서 실행하실 것을 권장합니다. 원서의 코드는 `/src`와 `/tests` 디렉터리에서 찾을 수 있습니다.

- 한국어판 저장소: https://github.com/TeeDDub/AI-Agent-Engineering
- 원서 저장소: https://github.com/michaelalbada/BuildingApplicationsWithAIAgents

## 빠른 시작: 새 컴퓨터에서 로컬 환경 재현

API 키 없이 모든 실습을 로컬에서 돌리는 순서입니다. 각 단계의 자세한 설명은 아래 '환경 설정'에 있습니다.

```bash
# 1) 도구 설치 (MacOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
brew install llama.cpp
# Docker Desktop 설치 후 실행: https://www.docker.com/products/docker-desktop/

# 2) 의존성과 .env
uv sync
source .venv/bin/activate
cp .env.example .env          # 이후 .env의 '로컬 모델' 블록 주석 해제 (5단계)

# 3) 모델 다운로드 — Hugging Face에서 직접 받습니다 (Ollama/LM Studio 불필요)
scripts/start_local_llm.sh --download    # LLM(약 17.6GB) + 임베딩(약 2.3GB). 수 분~수십 분 소요

# 4) 로컬 LLM 서버 — 별도 터미널에서 실행하고 계속 켜 둡니다
scripts/start_local_llm.sh

# 5) 관측 스택 — 8~9장에 필요
(cd src/common/observability && docker compose up -d)

# 6) 동작 확인
python ch04/calculator_tool_use.py
```

컴퓨터를 재시작하면 4)의 LLM 서버와 Docker Desktop을 다시 켜야 합니다. LLM 서버가 꺼져 있으면 예제가 시작할 때 `LocalLLMServerUnavailable` 오류와 함께 해결 방법을 안내합니다.

## 환경 설정

이 프로젝트는 패키지 매니저로 [uv](https://github.com/astral-sh/uv)를 사용합니다.

### 1. uv 설치

`uv`가 설치되어 있지 않다면 공식 문서를 참고하여 설치해주세요.

```bash
# MacOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 프로젝트 설정

프로젝트 루트에서 다음 명령어를 실행하여 가상환경을 생성하고 의존성을 설치합니다.

```bash
uv sync
```

이 명령어는 `.venv` 디렉토리에 가상환경을 생성하고, `uv.lock`에 정의된 패키지들을 설치합니다.

### 3. 가상환경 활성화

```bash
# MacOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4. 환경 변수 (`.env`)

```bash
cp .env.example .env
```

`.env`는 git에 올라가지 않습니다. API 키는 반드시 `.env`에만 넣으세요(`.env.example`은 저장소에 커밋되는 템플릿입니다).

LLM은 두 가지 방식 중 하나로 실행할 수 있습니다.

- **OpenAI API**: `.env`에 `OPENAI_API_KEY`만 설정하면 각 예제에 지정된 원래 모델(gpt-4o, gpt-5-mini 등)로 실행됩니다.
- **로컬 모델**: 아래 5단계를 따르면 API 키 없이 실행됩니다.

모든 예제는 `src/common/llm.py`를 통해 모델을 생성하므로, 코드 수정 없이 `.env`만으로 전환됩니다.

### 5. (선택) 로컬 모델로 실행

Hugging Face에서 받은 GGUF 모델을 [llama.cpp](https://github.com/ggml-org/llama.cpp)의 `llama-server`로 띄워 OpenAI 호환 API(`http://localhost:1234/v1`)로 사용합니다. 임베딩은 sentence-transformers로 프로세스 안에서 실행됩니다.

```bash
# llama.cpp 설치 (MacOS). Linux는 llama.cpp 릴리스 바이너리를 사용하세요.
brew install llama.cpp

# 모델 미리 받기 (선택). 받지 않으면 서버 첫 실행 때 LLM을, 예제 첫 실행 때 임베딩을 받습니다.
# 모두 ~/.cache/huggingface에 저장되며 서버와 예제가 같은 캐시를 사용합니다.
scripts/start_local_llm.sh --download           # Qwen3.8-27B + bge-m3 + all-MiniLM-L6-v2
scripts/start_local_llm.sh --download gpt-oss   # gpt-oss-20b + 임베딩

# LLM 서버 실행
scripts/start_local_llm.sh           # Qwen3.8-27B (기본, 약 17.6GB, 한국어 응답 품질 우수)
scripts/start_local_llm.sh gpt-oss   # gpt-oss-20b (약 12GB, 더 빠름)

# 그 밖의 Hugging Face GGUF 모델: <저장소>[:양자화] [파일.gguf] [llama-server 추가 인자...]
scripts/start_local_llm.sh --download unsloth/gemma-4-26b-a4b-it-GGUF:Q4_K_M
scripts/start_local_llm.sh unsloth/gemma-4-26b-a4b-it-GGUF:Q4_K_M
scripts/start_local_llm.sh --help
```

포트와 컨텍스트 길이는 `LLM_PORT`(기본 1234), `LLM_CTX`(기본 32768) 환경 변수로 바꿀 수 있습니다. 포트를 바꾸면 `.env`의 `OPENAI_BASE_URL`도 함께 바꾸세요.

`.env`에서 '로컬 모델' 블록의 주석을 해제하고, 위쪽의 `OPENAI_API_KEY=...` 줄은 지웁니다.

```bash
OPENAI_API_KEY=local                       # 로컬 서버는 키를 검사하지 않지만 값은 필요합니다
OPENAI_BASE_URL=http://localhost:1234/v1
LLM_MODEL=qwen3.8-27b                      # 표시용 이름. llama-server는 띄운 모델로 응답합니다
EMBEDDING_PROVIDER=huggingface
EMBEDDING_MODEL=BAAI/bge-m3                # 다국어 임베딩. 첫 사용 시 약 2.3GB 다운로드
```

- 이 블록을 다시 주석 처리하고 실제 `OPENAI_API_KEY`를 넣으면 OpenAI API로 돌아갑니다.
- 참고 사양: Apple M1 Max 64GB에서 검증했습니다. Qwen3.8-27B는 약 20GB, gpt-oss-20b는 약 13GB의 여유 메모리가 필요합니다.
- 서버 종료: `pkill llama-server`
- 다른 모델/서버: 코드는 특정 모델에 묶여 있지 않습니다. tool calling을 지원하는 모델을 OpenAI 호환 API로 띄우면(Ollama, LM Studio, vLLM 등) `OPENAI_BASE_URL`과 `LLM_MODEL`만 바꿔 사용할 수 있습니다. 임베딩은 sentence-transformers로 로드되는 Hugging Face 모델이면 `EMBEDDING_MODEL`로 바꿀 수 있습니다.

**서버가 꺼져 있을 때**: `OPENAI_BASE_URL`이 localhost를 가리키는데 서버에 연결할 수 없으면, 예제는 LLM을 만들 때 바로 다음 오류로 종료됩니다.

```text
LocalLLMServerUnavailable: 로컬 LLM 서버(http://localhost:1234/v1)에 연결할 수 없습니다.
  - 로컬 모델 사용: 다른 터미널에서 scripts/start_local_llm.sh 를 실행하세요.
  - OpenAI API 사용: .env에서 OPENAI_BASE_URL을 지우고 OPENAI_API_KEY를 설정하세요.
```

`scripts/start_local_llm.sh` 로그에 `server is listening on http://127.0.0.1:1234`가 출력된 뒤 다시 실행하세요. 첫 실행은 모델 다운로드가 끝나야 이 메시지가 나옵니다.

### 6. (선택) 관측 가능성 스택: Loki · Tempo · Grafana

8~9장 에이전트는 실행 로그를 Loki(`localhost:3100`)로 전송하므로, **Loki가 떠 있지 않으면 `ConnectionError`로 종료됩니다.** [Docker Desktop](https://www.docker.com/products/docker-desktop/)을 설치·실행한 뒤 다음을 실행합니다.

```bash
cd src/common/observability
docker compose up -d     # 종료: docker compose down
```

| 서비스 | 주소 | 역할 |
|---|---|---|
| Grafana | http://localhost:3000 (admin / admin) | 로그·트레이스 조회 UI |
| Loki | localhost:3100 | 로그 저장 (`log_to_loki`) |
| Tempo | localhost:3200 (조회), 4317/4318 (OTLP 수신) | 트레이스 저장 |
| Promtail | - | 로그 파일 수집 |

Grafana에서 **Connections → Data sources → Add**로 데이터 소스를 추가합니다. 컨테이너끼리는 서비스 이름으로 접근하므로 URL은 `localhost`가 아닙니다.

- Loki: `http://loki:3100`
- Tempo: `http://tempo:3200`

8~11장 에이전트는 Traceloop으로 트레이스를 남깁니다. `.env.example`의 기본값대로 두면 Traceloop API 키 없이 로컬 Tempo(`localhost:4318`)로 전송되고, Grafana의 Tempo 데이터 소스에서 조회할 수 있습니다.

```bash
TRACELOOP_API_KEY=
TRACELOOP_BASE_URL=http://localhost:4318
TRACELOOP_METRICS_ENABLED=false
```

LangSmith로 LLM 호출 흐름(프롬프트, tool call)을 보려면 `.env`에 `LANGCHAIN_TRACING_V2=true`와 [LangSmith](https://smith.langchain.com) API 키를 설정합니다. 무료 플랜으로 충분합니다.

## 예시 실행

가상환경을 활성화한 상태로 **프로젝트 루트에서** 실행합니다. 일부 예제(4장 MCP 등)가 루트 기준 상대 경로를 사용합니다.

```bash
python ch04/calculator_tool_use.py
python ch08/supply_chain_logistics_agent.py
```

9~11장 스크립트는 `.env`를 직접 읽지 않으므로 `--env-file`로 전달합니다.

```bash
uv run --env-file .env python ch09/agents/it_helpdesk_agent.py
```

### 장별 추가 준비 사항

기본 `uv sync`에 포함되지 않거나 외부 서비스가 필요한 예제입니다. 자세한 내용은 각 장의 `README.md`를 참고하세요.

| 장 | 예제 | 필요 사항 |
|---|---|---|
| 3장 | `realtime_voice_agent.py` | OpenAI Realtime API 전용 (로컬 모델 대체 불가) |
| 4장 | `langgraph_mcp_client.py` | 날씨 MCP 서버를 별도 터미널에서 실행 (`python ch04/mcp_servers/MCP_weather_server.py`) |
| 5장 | `basic_skill_selection.py` 등 | `WOLFRAM_ALPHA_APP_ID`, `YOUR_SLACK_BOT_TOKEN` |
| 6장 | `graphrag_test.sh` | 스크립트가 graphrag를 직접 설치 |
| 7장 | 파인튜닝 (SFT, DPO, RLVR) | `uv sync --extra fine-tuning` |
| 8장 | Redis / Ray / Temporal 멀티 에이전트 | 각 서버와 패키지(`ray`, `"redis<8"`, `temporalio`) 별도 설치. 상세는 `ch08/README.md` |
| 8~9장 | 에이전트 전반 | 6단계의 Loki |
| 11장 | `optimize_*.py` | `dspy[optuna]` 별도 설치 (MIPROv2에 `optuna` 필요) |
| 12장 | `prompt_injection_block.py` | `llm-guard` 별도 설치 |

### 로컬 모델 사용 시 제약

- 노트북(`notebook/`)의 임베딩 셀은 OpenAI 임베딩을 직접 호출하므로 로컬 모드에서 동작하지 않습니다. 채팅 모델 셀은 `.env`를 읽는 노트북(2~8장)에서 로컬 서버로 실행됩니다.
- 27B급 로컬 모델은 OpenAI API보다 느립니다. 호출이 많은 예제(예: `ch07.experiential_learning`)는 수 분 이상 걸릴 수 있습니다.

## 테스트

```bash
PYTHONPATH=src:. pytest tests --ignore=tests/fine_tuning --ignore=tests/frameworks
```

`tests/fine_tuning`은 `fine-tuning` extra가 필요하고, `tests/frameworks`는 현재 LangChain 1.x에서 제거된 `langchain.schema`를 import하므로 제외합니다.

