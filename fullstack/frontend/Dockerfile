# 1. Node.js 기반으로 빌드
FROM node:18

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 패키지 설치 및 빌드
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# 4. Nginx 설정 추가
FROM nginx:latest
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
