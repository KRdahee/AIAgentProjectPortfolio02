# test_agent.py
from agents.refactor import RefactoringAgent

if __name__ == "__main__":
    agent = RefactoringAgent()
    dummy_issue = "Bug: Null pointer exception in main calculation loop."
    dummy_code = "def old_code(): pass"
    
    response = agent.analyze_and_refactor(dummy_issue, dummy_code)
    print("✨ 에이전트 분석 및 리팩토링 결과 스키마:")
    for key, value in response.items():
        print(f"[{key}]:\n{value}\n")