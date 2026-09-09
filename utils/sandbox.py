import docker
import tempfile
import os

class DockerSandbox:
    def __init__(self):
        """ 
        Windows 및 다양한 운영체제 환경에 맞춘 명시적 Docker 데몬 연결 설정 
        Windows 환경에서는 환경 변수 방식과 파이프 방식을 순차적으로 시도합니다.
        """
        try:
            self.client = docker.from_env()
        except Exception:
            try:
                self.client = docker.DockerClient(base_url='npipe:////./pipe/docker_engine')
            except Exception as e:
                print(f"⚠️ Docker 데몬 연결 실패: {e}")
                self.client = None

    def run_tests_securely(self, source_code: str, test_code: str) -> dict:
        """
        임시 디렉토리를 생성하여 코드와 테스트 파일을 기록한 뒤, 
        네트워크가 격리된 Docker 볼륨으로 마운트하여 안전하게 pytest를 실행합니다.
        """
        if not self.client:
            return {"passed": False, "log": "Docker client is not initialized or Docker Desktop is down."}

        # 1회용 임시 디렉토리 생성
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = os.path.join(temp_dir, "main_code.py")
            test_path = os.path.join(temp_dir, "test_code.py")

            # 소스 코드 파일 쓰기
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(source_code)
                
            # 테스트 코드 파일 쓰기 (메인 코드를 import 하도록 헤더 추가)
            with open(test_path, "w", encoding="utf-8") as f:
                f.write("from main_code import *\n\n" + test_code)

            print("🛡️ [Security] Docker 샌드박스 격리 컨테이너 생성 및 TDD 테스트 실행 중...")

            try:
                container_logs = self.client.containers.run(
                    image="python:3.10-alpine",
                    command="sh -c 'pip install pytest --no-cache-dir && pytest /app/test_code.py'",
                    volumes={temp_dir: {"bind": "/app", "mode": "ro"}},
                    working_dir="/app",
                    remove=True,
                    network_disabled=True,
                    mem_limit="128m",
                    stderr=True,
                    stdout=True
                )
                
                log_output = container_logs.decode("utf-8")
                print("✅ [Security] 샌드박스 테스트 통과 완료")
                return {"passed": True, "log": log_output}

            except docker.errors.ContainerError as e:
                error_output = e.stderr.decode("utf-8") if e.stderr else str(e)
                print("❌ [Security] 샌드박스 내 테스트 실패 혹은 에러 검출")
                return {"passed": False, "log": error_output}
            
            except Exception as e:
                return {"passed": False, "log": f"Sandbox execution error: {str(e)}"}