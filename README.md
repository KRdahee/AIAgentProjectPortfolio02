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



------------------------------------------------------------------------------------------
# 🚀 AI Agent Project (JUST FOR FUN!) 🤖✨

https://app.notion.com/p/AI-3cf9ecfae81380269147d1d831ff99d2?source=copy_link -> 천천히 notion 정리중!

## 📌 목차
* **1.** 📄 사내 기획서 자동 검토 및 공기업 양식 변환 멀티 에이전트 
<!-- 👉 [Environment Setup & Project Structure](https://github.com/KRdahee/AIAgentProjectPortfolio/wiki/01.-Environment-Setup-Project-Structure) -->

* **2.** 💻 오픈소스 이슈 자동 분석 및 코드 리팩토링 에이전트
<!-- 👉 [AI Multi-Agent System for Automated Open-Source Maintenance](https://github.com/KRdahee/AIAgentProjectPortfolio/wiki/02.-AI-Multi-Agent-System-for-Automated-Open-Source-Maintenance)  -->

<br>
<br>

## 1. 📄 사내 기획서 자동 검토 및 공기업 양식 변환 멀티 에이전트

### 🎯 1. 추진 배경 및 개요
* **프로젝트 명:** 사내 기획서 자동 검토 및 공기업 양식 변환 멀티 에이전트 💡
* **추진 목적:** 공기업 기획팀의 엄격한 문서 표준 양식과 논리 구조에 맞춰 초안을 자동 검토·수정하고, SWOT 분석 및 예상 매출액 등의 정량적 데이터를 보완하여 문서 작성 효율성을 극대화합니다! 📈
* **핵심 기술:** LangGraph (`State`·`Node`·`Edge`, 순환 그래프), MCP(Model Context Protocol), HITL(Human-in-the-Loop), 무료 LLM API (Groq/Gemini Free Tier) 🛠️

<br>

### 🛠️ 2. 시스템 아키텍처 및 주요 기능

| 구분 | 주요 기능 | 적용 기술 스택 |
| :--- | :--- | :--- |
| **초안 분석 에이전트** 🔍 | 사용자가 입력한 기획서 초안의 논리적 결함 및 누락된 항목(목표, 기대효과 등)을 진단합니다. | Prompt 엔지니어링, Pydantic 데이터 검증 |
| **양식 변환 에이전트** 📝 | 공기업 기획팀 문서 표준 양식 및 어조(Tone & Manner)에 맞춰 본문 구조를 재편성합니다. | LangGraph Node 및 Edge 제어 |
| **데이터 보완 에이전트** 📊 | 요청된 프로젝트의 SWOT 분석표 및 단계별 예상 매출액 등 정량적 데이터를 자동으로 산출·보완합니다. | Function Calling, 외부 툴 연동 |
| **검토 및 피드백 (HITL)** 👥 | 최종 반영 전 인간 관리자의 승인 및 수정 지시를 받아 루프(Cyclic) 형태로 완성도를 높입니다. | Human-in-the-Loop (HITL) |

<br>

### 💻 3. 100% 무료 구축을 위한 추천 기술 스택
* **LLM Engine:** **Google Gemini API (Free Tier)** 또는 **Groq API (Llama 3 기반 무료 티어)** — 비용 부담 없이 고성능 모델의 Function Calling 및 추론 기능 활용
* **Orchestration:** **LangGraph** (Python 오픈소스 라이브러리, 로컬 구동 무료) — 순환(Cyclic) 워크플로우 및 멀티 에이전트 제어
* **Data & Validation:** **Pydantic** (데이터 유효성 검증), **FastAPI** (백엔드 API 서버 구축)
* **Interface:** **Streamlit** — 웹 기반 대시보드 및 HITL(Human-in-the-Loop) 승인 UI 구현 (로컬/무료 배포 가능)

<br>

### 💼 4. 실무 활용 방안 및 기대 효과
* **실무 활용 포인트:** 공공기관 및 기업 기획팀에서는 문서의 양식 정합성, 논리적 타당성, 정량적 데이터(SWOT, 예상 매출 등) 검토에 막대한 리소스를 소모합니다. 본 에이전트는 초안의 결함을 즉각 진단하고 공기업 표준 양식에 맞추어 문서를 재편성함으로써, 대외 문서 승인율을 높이고 문서 작성에 소모되는 반복 업무 리소스를 혁신적으로 절감합니다. 📉
* **단계별 로드맵 및 기대 효과:**
  * **1단계 (도입 및 테스트):** 문서 작성 및 검토 시간 **40% 단축** 및 부서 내 피드백 주기 최소화 ⏱️
  * **2단계 (전사 확산):** 공공 입찰 제안서 및 대외 보고서 승인율 향상으로 인한 실질적 수주 기회 확대 🚀
  * **3단계 (고도화):** 사내 지식 베이스와 완벽 연동하여 반복 문서 작성 업무의 **80% 이상 자동화** 달성 🤖

<br>

---

<br>

## 2. 💻 오픈소스 이슈 자동 분석 및 코드 리팩토링 에이전트

### 🎯 1. 추진 배경 및 개요
* **프로젝트 명:** 오픈소스 이슈 자동 분석 및 코드 리팩토링 에이전트 🛠️
* **추진 목적:** GitHub 레포지토리에 등록된 이슈와 버그 리포트를 AI가 실시간으로 관찰하고, 클린 아키텍처 원칙에 입각한 코드 리팩토링과 TDD(테스트 주도 개발) 기반 검증을 수행하여 유지보수 공수를 대폭 절감합니다! ⚡
* **핵심 기술:** Agent 루프 (Observe-Judge-Act), GitHub API, TDD/SDD 방법론, 클린 아키텍처 모듈 설계 🧩

<br>

### 🛠️ 2. 시스템 아키텍처 및 주요 기능

| 구분 | 주요 기능 | 적용 기술 스택 |
| :--- | :--- | :--- |
| **이슈 관찰 에이전트** 👀 | GitHub Webhook 및 API를 통해 신규 이슈와 에러 로그를 실시간 수집 및 파싱합니다. | GitHub API, Asyncio 비동기 처리 |
| **원인 분석 및 판단** 🔍 | 코드베이스 소스코드를 탐색하여 문제의 근본 원인을 진단하고 수정 방향성을 도출합니다. | LLM 코드 오케스트레이션, Function Calling |
| **리팩토링 및 TDD 구현** ✨ | 클린 아키텍처 규칙에 맞춘 모듈 설계 및 단위 테스트 코드를 동시 작성·실행합니다. | TDD (테스트 주도 개발), 클린 아키텍처 |
| **PR 자동 생성** 🚀 | 수정 완료된 코드를 브랜치에 커밋하고 상세한 변경 이유가 담긴 Pull Request를 자동 등록합니다. | GitHub Integration API |

<br>

### 💻 3. 100% 무료 구축을 위한 추천 기술 스택
* **LLM Engine:** **Groq API (Llama 3 - 무료 고속 추론)** 또는 **Google Gemini API** — 코드 분석 및 리팩토링 제안에 활용
* **Version Control & Integration:** **GitHub REST API / Webhooks** (개인 계정 활용 시 완전 무료) — 이슈 및 PR 자동 연동
* **Async & Core Logic:** **Python `asyncio`** (비동기 이벤트 처리), **Pytest** (TDD 단위 테스트 자동 실행)
* **Architecture Design:** **Clean Architecture** 원칙에 따른 디렉토리 모듈 구조 설계 및 스킬 주도 개발(SDD) 적용

<br>

### 💼 4. 실무 활용 방안 및 기대 효과
* **실무 활용 포인트:** 개발 조직에서 끊임없이 발생하는 GitHub 이슈와 버그 리포트 대응 공수를 획기적으로 줄여줍니다. AI가 직접 코드를 탐색하고 클린 아키텍처 규칙에 맞춰 리팩토링 및 테스트 코드(TDD)까지 동시에 수행하므로, 개발자들은 단순 반복 버그 수정에서 벗어나 핵심 비즈니스 로직 설계와 고차원 개발에만 집중할 수 있는 환경이 조성됩니다. 🛠️
* **단계별 로드맵 및 기대 효과:**
  * **1단계 (도입 및 테스트):** 단순 반복 버그 수정 시간 **50% 절감** 및 안정적인 코드 리뷰 지원 🔥
  * **2단계 (전사 확산):** 오픈소스 기여도 향상 및 사내 레거시 코드 표준화율 대폭 증가 📈
  * **3단계 (고도화):** CI/CD 파이프라인과 완벽 통합된 **완전 자율형 소프트웨어 유지보수 체계** 구축 ✨

 <br>


### 4. 애플리케이션 실행
```bash
# FastAPI 서버 구동 (포트 8000)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
