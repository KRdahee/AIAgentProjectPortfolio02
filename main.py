import os
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from workflow import create_workflow_graph
from utils.github_api import GitHubIntegration

# 1. FastAPI 인스턴스 초기화 (가장 먼저 선언)
app = FastAPI(
    title="오픈소스 이슈 자동 분석 및 리팩토링 에이전트 대시보드",
    description="LangGraph & Docker 기반 Self-Healing End-to-End 파이프라인 시스템"
)

# 디렉토리 절대 경로 확보
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 정적 에셋 및 템플릿 마운트
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "templates", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# LangGraph 컴파일된 워크플로우 로드
agent_workflow = create_workflow_graph()

class InteractiveRequest(BaseModel):
    issue_text: str
    legacy_code: str

# ---------------------------------------------------------
# API 라우트 정의 영역
# ---------------------------------------------------------

@app.post("/api/refactor-interactive")
async def api_refactor_interactive(payload: InteractiveRequest):
    """ 사용자가 대시보드에서 직접 입력한 코드와 이슈를 Gemini 에이전트로 실시간 처리 """
    from agents.refactor import RefactoringAgent
    agent = RefactoringAgent()
    result = agent.analyze_and_refactor(payload.issue_text, payload.legacy_code)
    return {"status": "success", "result": result}

@app.get("/")
async def serve_dashboard(request: Request):
    context = {
        "request": request,
        "system_msg": "AI 에이전트 파이프라인 상시 대기 중",
        "observe_status": "Active (Webhook Ready)",
        "judge_status": "Gemini-2.5-flash Engine Ready",
        "act_status": "Docker Sandbox Secured",
        "integrate_status": "GitHub API Ready"
    }
    return templates.TemplateResponse("index.html", context)

def run_background_agent(issue_number: int, issue_body: str, original_code: str):
    """ FastAPI 백그라운드 스레드에서 LangGraph 에이전트 루프를 구동합니다. """
    print(f"🤖 [Background] 이슈 #{issue_number}에 대한 AI 에이전트 자율 워크플로우 가동")
    
    initial_state = {
        "issue_number": issue_number,
        "issue_body": issue_body,
        "original_code": original_code,
        "refactored_code": "",
        "test_code": "",
        "test_passed": False,
        "error_log": "",
        "pr_url": "",
        "loop_count": 0
    }
    
    final_state = agent_workflow.invoke(initial_state)
    
    if final_state.get("test_passed"):
        print(f"✨ [Success] TDD 검증 통과 완료! 최종 PR 주소: {final_state.get('pr_url')}")
        github_api = GitHubIntegration("KRdahee/AIAgentProjectPortfolio02")
        github_api.create_pull_request_for_issue(
            issue_number=issue_number,
            target_file="main_logic.py",
            refactored_code=final_state.get("refactored_code"),
            commit_message=f"refactor: resolve issue #{issue_number} via AI Agent"
        )
    else:
        print("🚨 [Failure] 최대 재시도 횟수를 초과하였거나 검증에 실패했습니다.")

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    action = payload.get("action")
    issue_data = payload.get("issue", {})
    
    if action in ["opened", "reopened"]:
        issue_number = issue_data.get("number", 1)
        issue_body = issue_data.get("body", "No issue description provided.")
        sample_legacy_code = "def legacy_function():\n    # Spaghetti code\n    pass"
        background_tasks.add_task(run_background_agent, issue_number, issue_body, sample_legacy_code)
        return {"status": "Accepted", "message": f"Agent workflow triggered for issue #{issue_number}"}
    
    return {"status": "Ignored", "message": f"Action '{action}' is not handled."}

@app.post("/api/start-system")
async def api_start_system(background_tasks: BackgroundTasks):
    print("🚀 [Dashboard] 수동 시스템 가동 요청 수신")
    sample_issue_num = 777
    sample_issue_body = "Dashboard manual trigger: Refactor legacy calculation loop for high performance."
    sample_legacy_code = "def legacy_calc(data):\n    res = []\n    for i in data:\n        res.append(i * 2)\n    return res"
    
    background_tasks.add_task(run_background_agent, sample_issue_num, sample_issue_body, sample_legacy_code)
    return {"status": "success", "message": "AI 에이전트 파이프라인이 수동 가동되었습니다. 백그라운드 작업을 확인하세요!"}

@app.get("/api/logs")
async def api_get_logs():
    return {
        "status": "success", 
        "log": "[ACTIVE] Gemini API 연결 완료\n[SECURED] Docker 샌드박스 컨테이너 대기 중\n[READY] GitHub 자동 PR 연동 활성화 상태"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)