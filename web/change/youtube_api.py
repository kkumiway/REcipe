import os
import httpx
import json
from fastapi import HTTPException
from dotenv import load_dotenv
from fastapi_cache.decorator import cache
from urllib.parse import quote

# .env 파일 로드
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

@cache(expire=3600)  # 1시간 동안 캐싱 적용
async def get_youtube_video(menu_name: str):
    """YouTube API를 이용하여 특정 요리 관련 동영상 검색 (비동기 + 캐싱 + 최적화)"""

    if not YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="YouTube API Key가 설정되지 않음")

    params = {
        "part": "snippet",
        "q": f"{quote(menu_name)} 만드는 법",
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,  # 1개만 가져오기
        "type": "video"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:  # 타임아웃 설정 (속도 안정성)
            response = await client.get(YOUTUBE_SEARCH_URL, params=params)
        
        # ✅ 잘못된 API 키, 요청 초과 등의 예외 처리
        if response.status_code == 403:
            raise HTTPException(status_code=403, detail="YouTube API 요청 제한 초과 (Quota Exceeded)")

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="YouTube API 키가 잘못되었거나 권한 없음 (Invalid Credentials)")

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"YouTube API 요청 실패 (Error {response.status_code})")

        data = response.json()

        if "items" not in data or len(data["items"]) == 0:
            return {"title": None, "url": None}  # 검색 결과가 없을 경우 명확한 응답

        video_id = data["items"][0]["id"]["videoId"]
        video_title = data["items"][0]["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        return {"title": video_title, "url": video_url}

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="YouTube API 응답 시간 초과 (Gateway Timeout)")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"YouTube API 오류 발생: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"예상치 못한 오류 발생: {str(e)}")
