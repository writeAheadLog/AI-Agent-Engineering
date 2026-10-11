# Chapter 08: 멀티 에이전트 공급망 관리

이 디렉터리는 복잡한 공급망 및 물류 관리를 위해 여러 에이전트가 협력하는 시스템을 구축하는 방법을 다룹니다.

## 파일 목록

*   `supply_chain_logistics_agent.py`: LangGraph를 사용하여 재고, 운송, 공급업체 관리 등 다양한 도구를 활용하는 단일/멀티 에이전트 워크플로우의 기본 구현입니다.
*   `ray_supply_chain_multi_agent.py`: Ray 프레임워크를 사용하여 분산 환경에서 멀티 에이전트 공급망 시스템을 구동하는 예제입니다.
*   `temporal_supply_chain_multi_agent.py`: Temporal 워크플로우 엔진을 사용하여 내구성 있고 신뢰성 있는 멀티 에이전트 오케스트레이션을 구현한 예제입니다.
*   `adas/automated_design_of_agentic_systems.py`: 에이전트 시스템을 자동 설계(Automated Design of Agentic Systems, ADAS)하는 연구적 접근 방식을 보여주는 코드입니다.
*   `a2a/agent_server.py`: Agent-to-Agent 통신을 위한 서버 측 구현입니다.
*   `a2a/agent_client.py`: Agent-to-Agent 통신을 위한 클라이언트 측 구현입니다.

## 실행 방법

1.  [루트 README](../README.md)의 환경 설정 4~5단계에 따라 `.env`를 설정합니다 (OpenAI API 또는 로컬 모델).
2.  이 장의 에이전트는 실행 로그를 Loki로 보내므로, [루트 README](../README.md)의 6단계(관측 가능성 스택)를 먼저 실행합니다.
    Ray, Temporal, Redis 예제는 각 패키지와 서버를 별도로 설치·실행해야 합니다.
    *   Ray: `uv pip install ray` (서버 불필요, 로컬 클러스터 자동 실행)
    *   Redis: `docker run -d --name agent-redis -p 6379:6379 redis:7`, `uv pip install "redis<8"`
        (redis-py 8은 소켓 타임아웃 기본값이 5초라 예제의 `xread(block=5000)`과 충돌해 소비자 스레드가 종료됩니다.
        스트림에 이전 실행의 작업이 남아 있으면 먼저 처리하므로 재실행 전 `docker exec agent-redis redis-cli FLUSHALL`을 권장합니다.
        로컬 모델은 응답이 느려 90초 대기 시간을 넘길 수 있습니다.)
    *   Temporal: `brew install temporal`, `temporal server start-dev`, `uv pip install temporalio`
        (워커가 로컬 Temporal 서버 `localhost:7233`에 접속합니다.)
3.  기본 에이전트 실행:

```bash
python ch08/supply_chain_logistics_agent.py
```

4.  Ray 기반 멀티 에이전트 실행 (Ray 설치 필요):
```bash
python ch08/ray_supply_chain_multi_agent.py
```

5.  Temporal 기반 실행 (Temporal 서버 실행 필요):
```bash
python ch08/temporal_supply_chain_multi_agent.py
```
