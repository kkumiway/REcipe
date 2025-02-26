# API를 호출하지 않고 Mock 데이터로 테스트
import openai
from unittest.mock import MagicMock

# OpenAI API 키 설정 (API 없이 테스트할 때는 필요 없음)
openai.api_key = "your_api_key_here"

# Mock 데이터 설정
mock_response = {
    "choices": [
        {"message": {"content": '["닭고기", "감자"]'}}
    ]
}

# OpenAI API 호출을 Mock으로 대체
openai.ChatCompletion.create = MagicMock(return_value=mock_response)

# 함수 테스트 (실제 OpenAI API를 호출하지 않고 가짜 응답 사용)
def extract_ingredients(user_input):
    prompt = f"사용자가 입력한 문장에서 요리에 사용할 재료만 추출해 리스트로 반환해 줘.\n입력: {user_input}\n출력:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return eval(response["choices"][0]["message"]["content"])

# 실행 테스트
user_input = "닭고기랑 감자로 만들 수 있는 요리 알려줘."
result = extract_ingredients(user_input)
print(result)  # 예상 출력: ["닭고기", "감자"]


# API 호출 생략 후 코드의 흐름만 실행
def extract_ingredients(user_input, use_mock=True):
    if use_mock:
        return ["닭고기", "감자"]  # 실제 API 호출 없이 가짜 데이터 반환

    # 실제 API 호출 (나중에 활성화)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
    return eval(response["choices"][0]["message"]["content"])

# 테스트 실행
user_input = "닭고기랑 감자로 만들 수 있는 요리 알려줘."
ingredients = extract_ingredients(user_input, use_mock=True)  # 🔥 API 없이 실행
print(ingredients)  # 예상 출력: ["닭고기", "감자"]
