# 사용자 입력 처리 & OpenAI API 호출
from fastapi import APIRouter, Query # FastAPI에서 API 엔드포인트를 관리하는 라우터 객체 (모듈화를 위해 사용)
from services import generate_recipe_keywords # OpenAI API를 호출하여 요리 키워드 생성

# FastAPI의 라우터 객체 생성 -> 여러개의 엔드포인트 관리
router = APIRouter()

@router.get("/get_keywords") # GET 요청을 받을 엔트포인트 설정
def get_keywords(ingredient: str = Query(..., description="사용자가 입력한 재료")):
    """
    사용자 입력을 받아 OpenAI API 호출 → 관련 요리 키워드 생성 후 반환
    """
    keywords = generate_recipe_keywords(ingredient) # OpenAI API 호출하여 요리 키워드 생성
    
    return {"ingredient": ingredient, "generated_keywords": keywords} # JSON 형식으로 결과 반환
