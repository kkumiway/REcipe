from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_instagram_trends(ingredient):
    """ 인스타그램에서 입력된 재료와 관련된 인기 해시태그를 크롤링 """
    
    # 크롬 드라이버 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # 크롬 드라이버 실행 (크롬 드라이버 경로 지정 필요)
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 인스타그램 검색 URL 설정
    search_url = f"https://www.instagram.com/explore/tags/{ingredient}/"
    driver.get(search_url)
    
    # 페이지 로드 대기
    time.sleep(3)

    # 페이지 소스 가져오기
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # 인기 게시물에서 해시태그 가져오기
    hashtags = []
    for post in soup.find_all("a"):
        tag = post.get("href")
        if tag and "/explore/tags/" in tag:
            hashtags.append(tag.split("/")[-2])  # 해시태그만 추출
    
    # 드라이버 종료
    driver.quit()
    
    # 상위 5개 해시태그 반환
    return hashtags[:5] if hashtags else ["트렌드 없음"]