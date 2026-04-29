# 1단계 의존성 설치 스테이지:
# package.json / package-lock.json을 기준으로 node_modules를 재현 가능하게 설치하는 단계다.
# 이 단계를 분리하면 소스 코드가 바뀌어도 의존성 파일이 같을 때 Docker 캐시를 재사용할 수 있다.
FROM node:20-alpine AS deps

# 컨테이너 내부에서 프론트엔드 작업을 진행할 기본 디렉터리를 /app으로 정한다.
WORKDIR /app

# 의존성 정의 파일만 먼저 복사한다.
# 소스 전체보다 package-lock.json의 변경 빈도가 낮기 때문에 캐시 효율이 좋아진다.
COPY package.json package-lock.json ./

# lockfile 기준으로 정확한 버전의 패키지를 설치한다.
# npm ci는 CI/배포 환경에서 일관된 설치를 보장하는 용도에 적합하다.
RUN npm ci

# 2단계 빌드 스테이지:
# 앞 단계에서 설치한 node_modules를 재사용해 실제 Next.js 애플리케이션을 빌드한다.
FROM node:20-alpine AS builder

# 빌드 작업 기준 디렉터리를 /app으로 맞춘다.
WORKDIR /app

# 의존성 설치 스테이지에서 만들어진 node_modules를 그대로 가져온다.
# 이렇게 하면 이 단계에서 npm install을 다시 하지 않아도 된다.
COPY --from=deps /app/node_modules ./node_modules

# 현재 frontend 디렉터리의 프로젝트 파일을 컨테이너 내부로 복사한다.
# next.config.ts, app/router/pages, public, package.json 등이 여기 포함된다.
COPY . .

# Next.js telemetry 전송을 비활성화한다.
# 빌드/배포 환경에서 불필요한 통계 전송을 막기 위한 설정이다.
ENV NEXT_TELEMETRY_DISABLED=1

# Next.js 프로덕션 빌드를 수행한다.
# next.config.ts의 output: 'standalone' 설정 덕분에 실행에 필요한 최소 결과물이 .next/standalone에 생성된다.
RUN npm run build

# 3단계 실행 스테이지:
# 실제 서버에서 실행할 최소 구성만 담는 최종 이미지 단계다.
# 빌드 도구나 전체 소스 대신 standalone 결과물 중심으로 가져와 이미지 크기를 줄인다.
FROM node:20-alpine AS runner

# 실행 컨테이너의 기본 작업 디렉터리를 /app으로 설정한다.
WORKDIR /app

# 프로덕션 모드로 실행되도록 Node 환경 변수를 설정한다.
ENV NODE_ENV=production

# 런타임에서도 telemetry 전송을 비활성화한다.
ENV NEXT_TELEMETRY_DISABLED=1

# 보안을 위해 루트가 아닌 전용 그룹/사용자를 만든다.
# 이후 Next.js 서버 프로세스는 이 일반 사용자 권한으로 동작한다.
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# 정적 공개 자산(public 폴더)을 빌드 결과와 함께 복사한다.
# 이미지, favicon, robots.txt 같은 파일들이 여기에 해당한다.
COPY --from=builder /app/public ./public

# standalone 출력물을 현재 작업 디렉터리로 복사한다.
# --chown 옵션으로 파일 소유자를 nextjs:nodejs로 맞춰 권한 문제를 예방한다.
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./

# Next.js가 제공할 정적 빌드 산출물(.next/static)을 함께 복사한다.
# 이 디렉터리가 없으면 브라우저가 JS/CSS 정적 파일을 제대로 받지 못한다.
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 이후 컨테이너 내부 프로세스는 nextjs 사용자로 실행한다.
USER nextjs

# 애플리케이션이 3000번 포트를 사용함을 문서화한다.
EXPOSE 3000

# 런타임 포트를 3000으로 지정한다.
ENV PORT=3000

# 외부 요청을 받을 수 있도록 모든 인터페이스에 바인딩한다.
ENV HOSTNAME="0.0.0.0"

# standalone 빌드 결과에 포함된 server.js를 실행해 Next.js 서버를 시작한다.
CMD ["node", "server.js"]
