import os
from github import Github

class GitHubIntegration:
    def __init__(self, repo_name: str):
        """
        환경 변수에 등록된 GITHUB_TOKEN을 불러와 GitHub 클라이언트를 초기화합니다.
        repo_name 형식 예: "KRdahee/AIAgentProjectPortfolio02"
        """
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            print("⚠️ 경고: GITHUB_TOKEN이 설정되지 않았습니다.")
        
        self.g = Github(self.token)
        self.repo_name = repo_name

    def create_pull_request_for_issue(self, issue_number: int, target_file: str, refactored_code: str, commit_message: str) -> str:
        """
        1. 신규 리팩토링용 브랜치를 생성합니다.
        2. 타겟 파일을 수정된 코드로 업데이트(커밋)합니다.
        3. 원격 저장소로 푸시 후 Pull Request를 자동 개설하고 PR URL을 반환합니다.
        """
        if not self.token:
            return "https://github.com/mock-pr-url-due-to-no-token"

        try:
            repo = self.g.get_repo(self.repo_name)
            base_branch = repo.default_branch # 보통 main 또는 master
            new_branch_name = f"refactor/issue-{issue_number}"

            # 1. 브랜치 생성 (기본 브랜치의 최신 SHA 기준)
            base_ref = repo.get_branch(base_branch)
            try:
                repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=base_ref.commit.sha)
            except Exception:
                # 이미 브랜치가 존재하는 경우 우회 처리
                pass

            # 2. 파일 업데이트 및 커밋
            file_content = repo.get_contents(target_file, ref=base_branch)
            repo.update_file(
                path=target_file,
                message=commit_message,
                content=refactored_code,
                sha=file_content.sha,
                branch=new_branch_name
            )

            # 3. Pull Request 생성
            pr_title = f"[AI Refactor] 자동 리팩토링 및 TDD 검증 완료 (Issue #{issue_number})"
            pr_body = f"본 PR은 AI 오픈소스 리팩토링 에이전트에 의해 자동 생성되었습니다.\n- 대상 이슈 번호: #{issue_number}\n- 적용 원칙: 단일 책임 원칙(SRP) 및 클린 아키텍처"
            
            pull_request = repo.create_pull(
                title=pr_title,
                body=pr_body,
                head=new_branch_name,
                base=base_branch
            )

            print(f"🚀 [GitHub API] Pull Request 생성 성공: {pull_request.html_url}")
            return pull_request.html_url

        except Exception as e:
            print(f"❌ [GitHub API] PR 생성 중 오류 발생: {str(e)}")
            return f"Error creating PR: {str(e)}"