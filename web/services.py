# OpenAI API 호출 -> 요리 키워드 생성
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # //NOTE: 실제 OpenAI API 값이 입력되기 전

openai.api_key = OPENAI_API_KEY  # API 키 설정

def generate_recipe_keywords(ingredient: str):
    """
    OpenAI API를 호출하여 입력된 재료와 관련된 요리 키워드를 생성
    """
    # OpenAI 모델이 이해할 수 있도록 질문(프롬프트)을 만들기
    prompt = f"""
    다음 재료로 만들 수 있는 대표적인 요리 5개를 리스트로 알려줘:
    - {ingredient}
    """
    
    try:
        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # 사용할 OpenAI 모델
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )

        # 응답에서 요리 리스트 추출
        generated_text = response["choices"][0]["message"]["content"]
        recipe_keywords = [line.strip() for line in generated_text.split("\n") if line.strip()]
        # OpenAI API가 생성한 요리 키워드 리스트를 반환
        return recipe_keywords
    # 오류 처리
    except Exception as e:
        return {"error": str(e)}