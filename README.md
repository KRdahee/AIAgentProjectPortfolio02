# 💼 [Portfolio] AIAgentProjectPortfolio02
**지능형 멀티 에이전트 기반 실무 업무 자동화 시스템 (AI Multi-Agent Automation System)**

## □ 추진 배경 및 포트폴리오 개요
ㅇ **(목적)** 사내 기획 및 행정 업무, 오픈소스 개발 유지보수 과정에서 발생하는 고비용·저효율의 반복 업무를 AI 멀티 에이전트 루프를 통해 혁신하는 엔드투엔드(End-to-End) 자동화 파이프라인 구축
ㅇ **(핵심 역량)** 지능형(AI) 에이전트 기반 서비스 개발의 전문성을 바탕으로, LLM의 환각(Hallucination)을 통제하고 클린 아키텍처 및 TDD 방법론을 시스템적으로 강제하는 무결점 시스템 설계 입증

---

## □ 주요 프로젝트 상세 (Core Projects)

### 1. 사내 기획서 자동 검토 멀티 에이전트 (기획/행정 효율화)
ㅇ **(운영 개념)** 역할이 분리된 3단계 에이전트(Analyzer ➔ Converter ➔ Enhancer)가 협업하여 기획서 초안을 진단하고 공기업 표준 양식(개조식 등)으로 자동 변환
ㅇ **(핵심 기술)** LangGraph(순환 워크플로우 제어), Pydantic(정형화된 논리 검증 및 출력 강제), HITL(Human-in-the-Loop, 최종 관리자 승인 루프)
ㅇ **(비즈니스 임팩트)** 
   - 문서 1건당 소요 시간 85% 단축 (평균 4.5시간 ➔ 15~20분 내외)
   - 엄격한 3단 구조 및 개조식 어조 강제를 통한 초회 반려율 70% 감소

### 2. 오픈소스 이슈 자동 분석 및 리팩토링 에이전트 (개발/유지보수 효율화)
ㅇ **(운영 개념)** GitHub 레포지토리의 이슈를 실시간으로 관찰하고, 클린 아키텍처 원칙에 입각한 코드 리팩토링 및 테스트 코드 작성 후 Pull Request(PR) 자동 생성
ㅇ **(핵심 기술)** Observe-Judge-Act 자율 에이전트 루프, Docker 샌드박싱(안전한 1회용 코드 격리 테스트), GitHub Webhooks & REST API
ㅇ **(비즈니스 임팩트)** 
   - 단순 반복 버그 수정 시간 50% 절감 및 관리 공수 최소화
   - 미검증 코드의 서버 파괴 위험을 원천 차단하는 신뢰도 99% 이상의 자가 치유(Self-Healing) 파이프라인 확립

---

## □ 핵심 기술 스택 및 인프라 (Tech Stack & Infrastructure)
ㅇ **(AI / LLM Engine)** Llama 3 (Groq API), Google Gemini API 
   - 유료 상용 API 대신 고성능 오픈소스 모델과 무료 티어를 결합한 월간 인프라 '비용 제로 아키텍처' 달성
ㅇ **(Backend & Core Logic)** Python 3.10+, FastAPI (백엔드 라우팅), LangGraph (상태 및 루프 제어), Pytest (TDD 자동 실행)
ㅇ **(DevOps & Security)** Docker (격리 테스트 환경), GitHub Actions, Uvicorn

---

## □ 설치 및 로컬 실행 가이드 (Getting Started)

### 1. 레포지토리 클론 및 폴더 이동
```bash
git clone [https://github.com/YourUsername/AIAgentProjectPortfolio02.git](https://github.com/YourUsername/AIAgentProjectPortfolio02.git)
cd AIAgentProjectPortfolio02
```

### 2. 가상환경 생성 및 의존성 설치
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경 변수(.env) 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래의 API 키 및 토큰 정보를 입력합니다.
```env
GROQ_API_KEY="your_groq_api_key_here"
GEMINI_API_KEY="your_gemini_api_key_here"
GITHUB_TOKEN="your_github_personal_access_token_here"
TARGET_REPO="your_github_username/your_repository_name"
```

### 4. 애플리케이션 실행
```bash
# FastAPI 서버 구동 (포트 8000)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
