from fastapi import FastAPI
from llmcode.youtube_api import get_youtube_video
from llmcode.crowling import generate_recipe_from_trends
from llmcode.image import get_recipe_image
import json

app = FastAPI()

@app.get("/recipe/{ingredient}")
async def get_recipe(ingredient: str):
    """ 사용자가 재료 입력 → LLM이 요리 추천 → 유튜브 URL 자동 추가 """
    
    # ✅ LLM을 사용해 메뉴명과 레시피 생성 (다른 사람이 만든 코드)
    recipe = generate_recipe_from_trends(ingredient)
    
    try:
        recipe_json = json.loads(recipe)  # 🔥 JSON 변환
    except json.JSONDecodeError:
        return {"error": "Failed to parse recipe JSON from OpenAI API"}

    # ✅ YouTube API를 활용해 메뉴명에 맞는 유튜브 영상 불러오기
    youtube_video = get_youtube_video(recipe_json["menuName"])
    
    recipe_json["menuImage"] = get_recipe_image(recipe_json["menuName"])  

    # ✅ JSON 응답에 유튜브 링크 추가
    recipe_json["youtubeVideo"] = youtube_video  

    if isinstance(recipe_json["recipeInfo"], str):  
        recipe_json["recipeInfo"] = recipe_json["recipeInfo"].split("\n")
    # recipe_json["recipeInfo"] = recipe_json["recipeInfo"].split("\n")  

    return {
        "recipe": recipe_json
    }
# uvicorn llmcode.main:app --host 0.0.0.0 --port 8000 --reload