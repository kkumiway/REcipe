import requests
from bs4 import BeautifulSoup

def get_recipe_image(query):
    """Google 이미지 검색에서 첫 번째 이미지를 가져오기"""
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return "https://example.com/default.jpg"  # 검색 실패 시 기본 이미지
    
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")
    
    if len(img_tags) > 1:
        return img_tags[1]["src"]  # 첫 번째 이미지 URL 반환
    
    return "https://example.com/default.jpg"  # 이미지가 없을 경우 기본 이미지 반환

