# 1단계 빌드 스테이지 시작:
# Python 패키지를 설치하는 전용 단계이며, 최종 실행 이미지에 불필요한 빌드 흔적을 남기지 않기 위해 분리한다.
FROM python:3.11-slim AS builder

# 컨테이너 내부 기본 작업 디렉터리를 /app으로 설정한다.
# 이후 COPY, RUN 등의 상대 경로 기준점이 된다.
WORKDIR /app

# 의존성 목록 파일만 먼저 복사한다.
# 소스 코드보다 requirements.txt가 덜 자주 바뀌므로 Docker 레이어 캐시를 더 효율적으로 활용할 수 있다.
COPY requirements.txt .
# requirements.txt에 정의된 Python 패키지를 설치한다.
# 별도 --user 옵션 없이 시스템 기본 경로(/usr/local) 쪽에 설치해
# 이후 비루트 사용자(appuser)로 실행해도 실행 파일과 패키지에 접근할 수 있게 한다.
# --no-cache-dir 옵션으로 pip 캐시를 남기지 않아 이미지 용량을 줄인다.
RUN pip install --no-cache-dir -r requirements.txt

# 2단계 실행 스테이지 시작:
# 실제 서비스 실행에 필요한 최소한의 런타임 이미지를 새로 만든다.
FROM python:3.11-slim

# 실행 컨테이너의 기본 작업 디렉터리도 동일하게 /app으로 맞춘다.
WORKDIR /app

# 빌드 스테이지에서 /usr/local 아래 설치된 Python 패키지와 실행 파일을 복사한다.
# 이렇게 하면 실행 스테이지에서 다시 pip install 하지 않아도 되고,
# uvicorn 같은 실행 파일도 기본 PATH에서 바로 사용할 수 있다.
COPY --from=builder /usr/local /usr/local

# 애플리케이션 소스 코드를 컨테이너의 /app/app 경로로 복사한다.
COPY ./app ./app

# 보안을 위해 루트가 아닌 일반 사용자(appuser)를 생성한다.
# -m은 홈 디렉터리 생성, -u 1000은 사용자 ID를 고정해 권한 추적을 쉽게 한다.
# 이어서 /app 디렉터리 소유권을 appuser로 변경해 실행 중 권한 문제를 방지한다.
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
# 이후 명령과 컨테이너 실행 프로세스는 appuser 권한으로 동작한다.
USER appuser

# 애플리케이션이 8000 포트를 사용함을 문서화한다.
# 실제 포트 개방은 런타임 설정(docker run -p 등)에서 이루어진다.
EXPOSE 8000

# 컨테이너 시작 시 uvicorn으로 FastAPI 앱(app.main의 app 객체)을 실행한다.
# --host 0.0.0.0은 외부 요청을 받을 수 있도록 모든 네트워크 인터페이스에 바인딩한다.
# --port 8000은 서비스 포트를 8000으로 지정한다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
