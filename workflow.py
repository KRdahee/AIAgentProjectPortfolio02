from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.refactor import RefactoringAgent
from utils.sandbox import DockerSandbox

# ---------------------------------------------------------
# 1. 에이전트 상태(State) 정의
# ---------------------------------------------------------
class AgentWorkflowState(TypedDict):
    issue_number: int
    issue_body: str
    original_code: str
    refactored_code: Optional[str]
    test_code: Optional[str]
    test_passed: bool
    error_log: Optional[str]
    pr_url: Optional[str]
    loop_count: int  # 무한 루프 방지용 카운터

refactor_agent = RefactoringAgent()
sandbox = DockerSandbox()

# ---------------------------------------------------------
# 2. 노드(Node) 함수 정의
# ---------------------------------------------------------
def analyze_and_refactor_node(state: AgentWorkflowState):
    """ [Judge] 이슈를 분석하고 리팩토링 코드 및 테스트 코드를 생성/수정하는 노드 """
    current_loop = state.get("loop_count", 0) + 1
    print(f"\n--- [Judge] 리팩토링 에이전트 가동 (시도 횟수: {current_loop}회) ---")
    
    # 이전 단계에서 에러 로그가 존재한다면, 에러 피드백을 반영하여 재수정 로직 수행 가능
    error_log = state.get("error_log")
    if error_log:
        print(f"💡 [Self-Healing] 이전 테스트 에러 로그를 반영하여 코드를 보완합니다:\n{error_log[:200]}...")

    # 리팩토링 에이전트 호출
    result = refactor_agent.analyze_and_refactor(
        issue_body=state["issue_body"],
        original_code=state["original_code"]
    )
    
    return {
        "refactored_code": result["generated_code"],
        "test_code": result["test_code"],
        "loop_count": current_loop
    }

def run_tdd_tests_node(state: AgentWorkflowState):
    """ [Act] Docker 샌드박스에서 생성된 코드를 안전하게 테스트하는 노드 """
    print("--- [Act] Docker 샌드박스 내부에서 pytest 검증 진행 중 ---")
    
    result = sandbox.run_tests_securely(
        source_code=state["refactored_code"],
        test_code=state["test_code"]
    )
    
    return {
        "test_passed": result["passed"],
        "error_log": result["log"]
    }

def create_pull_request_node(state: AgentWorkflowState):
    """ [Act] 테스트 통과 시 GitHub Pull Request를 자동 생성하는 노드 """
    print("--- [Act] TDD 검증 통과! GitHub PR 자동 생성 진행 ---")
    # TODO: 추후 utils/github_api.py 연동
    mock_pr_url = f"https://github.com/repo/pull/{state['issue_number']}"
    return {"pr_url": mock_pr_url}

# ---------------------------------------------------------
# 3. 조건부 분기(Conditional Edge) 제어 함수
# ---------------------------------------------------------
def check_test_result(state: AgentWorkflowState):
    """ 테스트 결과 및 루프 횟수에 따라 다음 경로를 결정합니다. """
    if state.get("test_passed", False):
        return "passed"
    
    # 무한 루프 방지 (최대 3회 허용)
    if state.get("loop_count", 0) >= 3:
        print("🚨 [Alert] 최대 수정 횟수(3회) 초과. 무한 루프 방지를 위해 파이프라인을 중단합니다.")
        return "max_loops"
    
    print("🔄 [Self-Healing] 테스트 실패. 에러 로그를 가지고 리팩토링 단계로 회귀합니다.")
    return "failed"

# ---------------------------------------------------------
# 4. LangGraph 컴파일러 구성 함수
# ---------------------------------------------------------
def create_workflow_graph():
    workflow = StateGraph(AgentWorkflowState)

    # 노드 등록
    workflow.add_node("analyze_and_refactor", analyze_and_refactor_node)
    workflow.add_node("run_tdd_tests", run_tdd_tests_node)
    workflow.add_node("create_pull_request", create_pull_request_node)

    # 진입점 설정 및 직선 엣지 연결
    workflow.set_entry_point("analyze_and_refactor")
    workflow.add_edge("analyze_and_refactor", "run_tdd_tests")

    # 조건부 분기 설정 (TDD 결과에 따른 순환 루프)
    workflow.add_conditional_edges(
        "run_tdd_tests",
        check_test_result,
        {
            "passed": "create_pull_request",        # 테스트 통과 ➔ PR 생성
            "failed": "analyze_and_refactor",       # 테스트 실패 ➔ 리팩토링 노드로 재귀 (자가 치유)
            "max_loops": END                        # 제한 초과 ➔ 비상 종료
        }
    )
    workflow.add_edge("create_pull_request", END)

    return workflow.compile()