import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from urllib.parse import quote
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# ✅ OpenAI API 키 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_naver_blog_titles_multiple_pages(ingredient, max_pages=3):
    """Selenium을 사용하여 네이버 블로그에서 레시피 관련 게시글 제목과 URL 크롤링"""

    # Chrome WebDriver 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # GUI 없이 실행 (백그라운드 모드)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")  # 해상도 설정 (UI 깨짐 방지)

    # WebDriverManager를 사용하여 ChromeDriver 설치 최적화
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 5)  # 대기 시간을 5초로 설정 (최적화)

    # 검색어를 URL 인코딩하여 첫 번째 페이지 URL 설정
    encoded_ingredient = quote(ingredient)
    base_url = f"https://section.blog.naver.com/Search/Post.naver?keyword={encoded_ingredient}+레시피"
    driver.get(base_url)

    blog_data = []  # (제목, URL) 저장할 리스트
    previous_url = ""  # 중복 요청 방지를 위한 URL 저장

    try:
        for page in range(1, max_pages + 1):
            print(f"\n🔍 [크롤링 중: {page} 페이지]")

            # 중복 페이지 크롤링 방지
            if driver.current_url == previous_url:
                print("⚠️ 동일한 페이지가 반복 호출됨. 크롤링 종료.")
                break
            previous_url = driver.current_url

            # 페이지가 완전히 표시될 때까지 대기
            try:
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.title")))
            except TimeoutException:
                print("⚠️ 페이지 로딩이 너무 오래 걸립니다. 크롤링 종료.")
                break

            # BeautifulSoup을 사용하여 제목과 URL 함께 크롤링
            soup = BeautifulSoup(driver.page_source, "html.parser")
            posts = soup.select(".title_area")
            for post in posts:
                title = post.select_one("span.title").get_text(strip=True)
                link = post.find_parent("a")["href"]
                blog_data.append((title, link))

            # 다음 페이지 버튼 클릭 (비활성화 확인 후 클릭)
            try:
                page_button = driver.find_element(By.XPATH, '//a[contains(@class, "btn_next")]')
                if "disabled" in page_button.get_attribute("class"):
                    print("⚠️ 다음 페이지가 없습니다. 크롤링 종료.")
                    break
                driver.execute_script("arguments[0].click();", page_button)
                wait.until(EC.staleness_of(page_button))  # 새 페이지 로딩 대기
            except NoSuchElementException:
                print("⚠️ 다음 페이지 버튼이 없습니다. 크롤링 종료.")
                break
            except WebDriverException as e:
                print(f"⚠️ 웹드라이버 오류 발생: {e}")
                break
            except Exception as e:
                print(f"⚠️ 예상치 못한 오류 발생: {e}")
                break

    finally:
        if driver:
            driver.quit()  # 무조건 WebDriver 종료 (안정성 강화)

    return blog_data if blog_data else [("트렌드 없음", "N/A")]

# 실행
result = get_naver_blog_titles_multiple_pages("김치", max_pages=3)

# 네이버 블로그 크롤링 결과 출력
print("\n📌 네이버 블로그 크롤링 결과:")
for title, link in result:
    print(f"📍 {title} - {link}")
