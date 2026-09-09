import os
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

# .env 파일의 환경 변수 로드
load_dotenv()

# ---------------------------------------------------------
# 1. 에이전트 분석 결과 데이터 스키마 (Pydantic 구조화)
# ---------------------------------------------------------
class IssueAnalysisSchema(BaseModel):
    issue_number: int = Field(..., description="분석 중인 GitHub 이슈 번호")
    target_files: List[str] = Field(..., description="수정이 필요한 타겟 파일 경로 리스트")
    refactoring_plan: str = Field(..., description="클린 아키텍처 기반의 코드 수정 및 리팩토링 계획")
    generated_code: str = Field(..., description="단일 책임 원칙(SRP)이 적용된 수정 완료 코드")
    test_code: str = Field(..., description="수정된 코드를 검증하기 위한 pytest 기반 단위 테스트 코드")

# ---------------------------------------------------------
# 2. 리팩토링 에이전트 (Gemini API 탑재)
# ---------------------------------------------------------
class RefactoringAgent:
    def __init__(self):
        """ 
        Google GenAI SDK를 활용하여 Gemini 클라이언트를 초기화합니다.
        """
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
            
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-3.6-flash"

    def analyze_and_refactor(self, issue_body: str, original_code: str) -> dict:
        """
        Gemini 모델을 호출하여 구조화된 리팩토링 결과를 Pydantic 스키마로 반환합니다.
        """
        print(f"🔍 [Judge - Gemini] 이슈 분석 및 클린 아키텍처 기반 리팩토링 진행 중...")
        
        prompt = f"""
        당신은 수석 소프트웨어 아키텍트이자 리팩토링 전문 AI 에이전트입니다.
        아래의 GitHub 이슈와 원본 코드를 분석하여 단일 책임 원칙(SRP)과 클린 아키텍처에 맞게 코드를 리팩토링하고, pytest용 단위 테스트 코드를 작성해주세요.

        [GitHub Issue]:
        {issue_body}

        [Original Code]:
        {original_code}
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=IssueAnalysisSchema,
                    temperature=0.2,
                ),
            )
            
            result_data = IssueAnalysisSchema.model_validate_json(response.text)
            return result_data.model_dump()

        except Exception as e:
            print(f"⚠️ [Gemini API 오류 발생, Fallback Mock 데이터 반환]: {e}")
            fallback_result = IssueAnalysisSchema(
                issue_number=1,
                target_files=["main_logic.py"],
                refactoring_plan=f"API 호출 실패로 인한 예외 처리 및 기본 리팩토링 수행: {str(e)}",
                generated_code="def clean_function():\n    return 'gemini_fallback_executed'",
                test_code="def test_clean_function():\n    assert clean_function() == 'gemini_fallback_executed'"
            )
            return fallback_result.model_dump()