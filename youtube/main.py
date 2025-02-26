from fastapi import FastAPI
from youtube_api import get_youtube_video
from llm_recipe_generator import generate_recipe

app = FastAPI()

@app.get("/recipe/{ingredient}")
async def get_recipe(ingredient: str):
    """ 사용자가 재료 입력 → LLM이 요리 추천 → 유튜브 URL 자동 추가 """
    
    # ✅ LLM을 사용해 메뉴명과 레시피 생성 (다른 사람이 만든 코드)
    recipe = generate_recipe(ingredient)  

    # ✅ YouTube API를 활용해 메뉴명에 맞는 유튜브 영상 불러오기
    youtube_video = get_youtube_video(recipe["menuName"])
    
    # ✅ JSON 응답에 유튜브 링크 추가
    recipe["youtubeVideo"] = youtube_video  

    return recipe

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload