 # Selenium 임포트
from selenium import webdriver
import time

# 크롬 드라이버 생성 - 경로 설정 필요 없음
driver = webdriver.Chrome()
driver.implicitly_wait(3)

# 사이트 접속하기
driver.get('https://workey.codeit.kr/costagram/index')
time.sleep(1)

driver.find_element_by_css_selector('.top-nav__login-link').click()

driver.find_element_by_css_selector('.login-container__login-input').send_keys('codeit')
driver.find_element_by_css_selector('.login-container__password-input').send_keys('datascience')
driver.find_element_by_css_selector('.login-container__login-button').click()

last_height = driver.execute_script('return document.body.scrollHeight')

while True:
    # scrollHeight까지 스크롤
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    
    # 새로운 내용 로딩될때까지 기다림
    time.sleep(0.5)
    
    # 새로운 내용 로딩됐는지 확인
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

posts = driver.find_element_by_css_selector('.post-list__post')

for post in posts:
    # 썸네일 클릭
    post.click()
    time.sleep(0.5)
    
    # 닫기 버튼 클릭
    driver.find_element_by_css_selector('.close-btn').click()
    time.sleep(0.5)
    
driver.quit()
print(posts)
 

# branch_infos = []
# branch_elements = driver.find_elements_by_css_selector('div.branch')

# for branch_element in branch_elements:
#     branch_name = branch_element.find_element_by_css_selector('p.city').text
#     address = branch_element.find_element_by_css_selector('p.address').text
#     phone_number = branch_element.find_element_by_css_selector('span.phoneNum').text
#     branch_infos.append([branch_name, address, phone_number])
    
# driver.quit()

# print(branch_infos)