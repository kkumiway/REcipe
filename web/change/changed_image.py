import requests
from bs4 import BeautifulSoup

def get_recipe_image(query):
    """Google 이미지 검색에서 첫 번째 이미지를 가져오기 (속도 최적화)"""

    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Encoding": "gzip, deflate",  # 응답 압축 활성화 (속도 향상)
    }

    # `requests.Session()`을 사용하여 연결 재사용 (속도 향상)
    with requests.Session() as session:
        response = session.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return "https://example.com/default.jpg"  # 검색 실패 시 기본 이미지
    
    # `lxml`을 사용하여 더 빠르게 파싱
    soup = BeautifulSoup(response.content, "lxml")
    
    # 이미지 태그에서 `data-src`, `srcset`, `src` 순으로 탐색 (더 정확한 이미지 선택)
    img_tags = soup.find_all("img")
    
    for img in img_tags:
        img_url = img.get("data-src") or img.get("srcset") or img.get("src")
        if img_url and img_url.startswith("http"):  # 유효한 이미지 URL인지 확인
            return img_url  # 첫 번째 적절한 이미지 URL 반환

    return "https://example.com/default.jpg"  # 이미지가 없을 경우 기본 이미지 반환

# 실행 테스트
print(get_recipe_image("김치찌개"))
