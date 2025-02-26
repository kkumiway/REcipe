# 예시
def generate_recipe(ingredient: str):
    """LLM 없이 예제 데이터를 사용하여 요리 추천"""
    sample_recipes = {
        "양배추": {
            "menuName": "양배추 덮밥",
            "ingredients": "양배추, 간장, 마늘, 밥, 계란",
            "recipeInfo": "1. 양배추를 썬다...\n2. 팬에 볶아 간장을 넣는다.\n3. 밥 위에 올리고 계란을 추가한다."
        },
        "감자": {
            "menuName": "감자 볶음",
            "ingredients": "감자, 소금, 식용유, 마늘",
            "recipeInfo": "1. 감자를 채 썬다...\n2. 프라이팬에 볶는다."
        },
        "토마토": {
            "menuName": "토마토 스크램블",
            "ingredients": "토마토, 계란, 소금, 후추",
            "recipeInfo": "1. 토마토를 썬다...\n2. 계란과 함께 볶는다."
        }
    }

    return sample_recipes.get(ingredient, {
        "menuName": "알 수 없는 요리",
        "ingredients": "입력한 재료에 대한 추천이 없습니다.",
        "recipeInfo": "다른 재료를 입력해 주세요."
    })