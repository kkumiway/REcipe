import os
import openai
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# ✅ 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ LangChain의 ChatOpenAI 사용 (최적화된 모델 호출)
llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)


def get_naver_blog_titles_one_page(ingredient):
    """Selenium을 사용하여 네이버 블로그 첫 번째 페이지 크롤링"""

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

    print("\n🔍 [크롤링 중: 1 페이지]")

    # 페이지 로딩 대기 (JavaScript 실행을 위한 대기 시간)
    time.sleep(2)

    # 페이지 소스 가져오기
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 블로그 제목 크롤링
    blog_texts = []
    for post in soup.find_all("span", class_="title"):
        title = post.get_text(strip=True)  # HTML 태그 제거하고 텍스트만 추출
        blog_texts.append(title)

    driver.quit()
    return blog_texts if blog_texts else ["트렌드 없음"]



from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# ✅ 프롬프트 템플릿 설정
recipe_prompt = PromptTemplate(
    input_variables=["ingredient", "blog_texts"],
    template="""
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
)

# ✅ LangChain의 LLMChain을 사용하여 OpenAI API 최적화
recipe_chain = LLMChain(llm=llm, prompt=recipe_prompt)

def generate_recipe_from_trends(ingredient):
    """🔍 네이버 블로그 크롤링 후 LLM을 이용해 요리 레시피 생성"""
    
    # ✅ 내부에서 블로그 크롤링 실행 (중복 방지)
    blog_texts = get_naver_blog_titles_one_page(ingredient)

    # ✅ 크롤링한 데이터를 LangChain으로 전달
    response = recipe_chain.run(ingredient=ingredient, blog_texts=blog_texts)
    return response

# ✅ 실행 테스트
ingredient = "김치"
recipe = generate_recipe_from_trends(ingredient)  # 인수에서 blog_texts 제거!
print(recipe)