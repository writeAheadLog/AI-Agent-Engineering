# Chapter 09: 에이전트 평가 (Evaluation)

이 디렉터리는 에이전트의 성능, 도구 사용 정확도, 메모리 관리 능력 등을 정량적으로 평가하는 지표와 방법을 다룹니다.

## 파일 목록

*   `metrics.py`: 에이전트의 응답 정확도, 도구 호출 정밀도/재현율(Precision/Recall), 문구 일치도 등을 계산하는 다양한 평가 지표 함수들을 정의합니다. BERTScore, Cosine Similarity 등의 지표도 포함됩니다.
*   `memory_evaluation.py`: 에이전트의 메모리 업데이트 및 검색(Retrieval) 성능을 평가하기 위한 함수들을 포함합니다. 메모리 정밀도, 재현율, F1 점수 등을 계산합니다.

*   `agents/`: 평가 대상 도메인별 에이전트(고객 지원, 금융, 의료, IT 헬프데스크, 법무, SOC, 공급망)입니다.
*   `scenarios/`: 도메인별 평가 데이터셋(JSONL)입니다.
*   `batch_evaluation.py`: 에이전트를 시나리오 데이터셋으로 일괄 평가하는 스크립트입니다.

## 실행 방법

`metrics.py`와 `memory_evaluation.py`는 다른 코드에서 임포트하여 사용하는 모듈입니다.

1.  [루트 README](../README.md)의 환경 설정 4~5단계에 따라 `.env`를 설정합니다 (OpenAI API 또는 로컬 모델).
2.  에이전트는 실행 로그를 Loki로 보내므로, 루트 README의 6단계(관측 가능성 스택)를 먼저 실행합니다.
3.  이 장의 스크립트는 `.env`를 직접 읽지 않으므로 프로젝트 루트에서 `--env-file`로 전달합니다.

```bash
# 개별 에이전트 실행
uv run --env-file .env python ch09/agents/it_helpdesk_agent.py

# 시나리오 일괄 평가
uv run --env-file .env python ch09/batch_evaluation.py \
  --dataset ch09/scenarios/ecommerce_customer_support_evaluation_set.jsonl \
  --graph_py ch09/agents/customer_support_agent.py
```
