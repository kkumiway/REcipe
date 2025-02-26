# OpenAI API 호출 -> 요리 키워드 생성
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()  # 환경 변수 로드
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY  # API 키 설정

def generate_recipe_keywords(ingredient: str):
    """
    OpenAI API를 호출하여 입력된 재료와 관련된 요리 키워드를 생성
    """
    prompt = f"""
    다음 재료로 만들 수 있는 대표적인 한국 요리 5개를 리스트로 알려줘:
    - {ingredient}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )

        # 응답에서 요리 리스트 추출
        generated_text = response["choices"][0]["message"]["content"]
        recipe_keywords = [line.strip() for line in generated_text.split("\n") if line.strip()]

        return recipe_keywords

    except Exception as e:
        return {"error": str(e)}