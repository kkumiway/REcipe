# 사용자 입력 처리 & OpenAI API 호출
from fastapi import APIRouter, Query
from services import generate_recipe_keywords

router = APIRouter()

@router.get("/get_keywords")
def get_keywords(ingredient: str = Query(..., description="사용자가 입력한 재료")):
    """
    사용자 입력을 받아 OpenAI API 호출 → 관련 요리 키워드 생성 후 반환
    """
    keywords = generate_recipe_keywords(ingredient)
    
    return {"ingredient": ingredient, "generated_keywords": keywords}
