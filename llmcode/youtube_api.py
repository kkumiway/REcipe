import requests
import os
from fastapi import HTTPException
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def get_youtube_video(menu_name: str):
    """ YouTube API를 이용하여 특정 요리 관련 동영상 검색 """
    if not YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="YouTube API Key가 설정되지 않음")

    params = {
        "part": "snippet",
        "q": f"{menu_name} 만드는 법",
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,  # 1개만 가져오기
        "type": "video"
    }
    
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="YouTube API 요청 실패")
    
    data = response.json()
    
    if "items" not in data or len(data["items"]) == 0:
        return None  # 관련 영상 없음
    
    video_id = data["items"][0]["id"]["videoId"]
    video_title = data["items"][0]["snippet"]["title"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    video_id = data["items"][0]["id"]["videoId"]
    video_title = data["items"][0]["snippet"]["title"]
    video_thumbnail = data["items"][0]["snippet"]["thumbnails"]["high"]["url"]
    video_embed_url = f"https://www.youtube.com/embed/{video_id}"

    return {
        "title": video_title,
        "embed_url": video_embed_url,
        "thumbnail": video_thumbnail
    }

if __name__ == "__main__":
    menu_name = "김치볶음밥"
    result = get_youtube_video(menu_name)
    print(result)