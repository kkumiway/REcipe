import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
api_key = os.getenv("RECIPE_API_KEY")

print("API Key:", api_key)

# .env 파일 로드
load_dotenv()  

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("RECIPE_API_KEY")  

if api_key:
    print("API 키가 정상적으로 불러와졌습니다")
else:
    print("API 키가 없습니다. .env 파일을 확인하세요.")
