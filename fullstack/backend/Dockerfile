# 1. OpenJDK 21 사용
FROM openjdk:21-jdk-slim AS build

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 프로젝트 파일 복사
COPY . .

# 4. Gradle 실행 권한 부여
RUN chmod +x gradlew

# 5. Gradle 캐시 활용하여 빌드
RUN ./gradlew build --no-daemon -x test

# 6. 실행용 이미지 생성
FROM openjdk:21-jdk-slim

WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar

CMD ["java", "-jar", "app.jar"]

EXPOSE 8080
