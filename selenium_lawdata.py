# 이미지 파일 크롤링

from unittest import case
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import traceback
from selenium import webdriver
import time

import urllib3

# 워크북 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['사건구분', '키워드/결과', '승소 요지', '사건 개요', '변호사'])

# 크롬 드라이버 생성 - 경로 설정 필요 없음
driver = webdriver.Chrome()
driver.get("https://www.star-law.com/bbs/board.php?bo_table=case_starlaw")
elem = driver.find_element_by_name("q")

SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 1
for image in images:
    try:
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
        opener= urllib3.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib3.request.install_opener(opener)
        urllib3.request.urlretrieve(imgUrl, str(count) + ".jpg")
        count = count + 1
    except:
        pass

driver.close()

# case_division 사건 구분
# case_keyword 키워드
# case_victory_point 승소요지
# case_overview 사건 개요
# case_lawyer 변호사