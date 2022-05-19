import time
from selenium import webdriver

# 웹 드라이버 설정
driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get('https://workey.codeit.kr/costagram/index')
time.sleep(1)

# 로그인
driver.find_element_by_css_selector('.top-nav__login-link').click()
time.sleep(1)

driver.find_element_by_css_selector('.login-container__login-input').send_keys('codeit')
driver.find_element_by_css_selector('.login-container__password-input').send_keys('datascience')

driver.find_element_by_css_selector('.login-container__login-button').click()
time.sleep(1)

# 페이지 끝까지 스크롤
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(0.5)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 모든 썸네일 요소 가져오기
posts = driver.find_elements_by_css_selector('.post-list__post')

for post in posts:
    # 썸네일 클릭
    post.click()
    time.sleep(0.5)

    ### 코드를 작성하세요 ###
    style_attr = driver.find_element_by_css_selector('.post-container__image').get_attribute('style')
    image_url = style_attr.split('"')[1]
    print(image_url)

    # 닫기 버튼 클릭
    driver.find_element_by_css_selector('.close-btn').click()
    time.sleep(0.5)

driver.quit()