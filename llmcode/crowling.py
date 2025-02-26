import os
import time
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ✅ OpenAI API 키 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_naver_blog_titles_multiple_pages(ingredient, max_pages=3):
    """Selenium을 사용하여 네이버 블로그 여러 페이지 크롤링"""

    # Chrome WebDriver 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # GUI 없이 실행 (백그라운드 모드)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # ✅ WebDriverManager를 사용하여 chromedriver 자동 다운로드 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 검색어를 기반으로 첫 번째 페이지 URL 설정
    base_url = f"https://section.blog.naver.com/Search/Post.naver?keyword={ingredient}+레시피"
    driver.get(base_url)

    blog_texts = []  # 크롤링한 데이터를 저장할 리스트

    for page in range(1, max_pages + 1):
        print(f"\n🔍 [크롤링 중: {page} 페이지]")

        # 페이지 로딩 대기 (JavaScript 실행을 위한 대기 시간)
        time.sleep(5)

        # 페이지 소스 가져오기
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 블로그 제목 크롤링
        for post in soup.find_all("span", class_="title"):
            title = post.get_text(strip=True)  # HTML 태그 제거하고 텍스트만 추출
            blog_texts.append(title)

        # ✅ 페이지 버튼 클릭 (페이지 번호를 찾아 클릭)
        try:
            page_button = driver.find_element("xpath", f'//a[@aria-label="{page+1}페이지"]')  # 다음 페이지 버튼
            page_button.click()
            time.sleep(5)  # 페이지가 로딩될 시간을 기다림
        except:
            print("⚠️ 다음 페이지 버튼을 찾을 수 없음. 크롤링 종료.")
            break  # 더 이상 다음 페이지가 없으면 크롤링 종료

    driver.quit()
    return blog_texts if blog_texts else ["트렌드 없음"]

def generate_recipe_from_trends(ingredient):
    """네이버 블로그 데이터를 기반으로 OpenAI API로 요리 레시피 생성"""
    
    # ✅ 네이버 블로그에서 최신 요리 트렌드 가져오기
    blog_texts = get_naver_blog_titles_multiple_pages(ingredient)

    # ✅ OpenAI API 프롬프트 작성
    prompt = f"""
    다음은 네이버 블로그에서 '{ingredient}'와 관련된 최신 요리 트렌드 데이터입니다.
    {blog_texts}

    위 데이터를 기반으로, 현재 '{ingredient}'을 활용한 인기 요리를 하나 추천해주세요.
    그리고 아래 형식으로 JSON 데이터를 생성해주세요:

    {{
        "menuName": "추천된 요리 이름",
        "menuImage": "해당 요리를 나타내는 대표 이미지 URL",
        "ingredients": "해당 요리를 만들 때 필요한 주요 재료 (쉼표로 구분)",
        "recipeInfo": "요리하는 방법을 단계별로 설명",
        "menuTip": "더 맛있게 만드는 팁"
    }}

    JSON 형식만 출력하고, 설명 없이 반환해주세요.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content  # ✅ OpenAI API의 결과 반환
