from unittest import case
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import traceback
from selenium import webdriver
import time

# 워크북 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['사건구분', '키워드/결과', '승소 요지', '사건 개요', '변호사'])

# 크롬 드라이버 생성 - 경로 설정 필요 없음
driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get('http://www.yklaw.net/deteg/success/?&page=1')
time.sleep(1)

playlists = driver.find_elements_by_css_selector('/html/body/div[3]/div[2]/div/div[2]/div/div[3]/table/tbody/tr[2]/td[3]/a').click()

for playlist in playlists:
    case_division = ['']
    case_keyword = playlist.find_element_by_css_selector('').text
    case_victory_point = playlist.find_element_by_css_selector('').text
    case_overview = playlist.find_element_by_css_selector('').text
    case_lawyer = playlist.find_element_by_css_selector('').text
    
    ws.append([case_division, case_keyword, case_victory_point, case_overview, case_lawyer])
    
driver.quit()
wb.save('플레이리스트_정보.xlsx')
            

wb.save('록션_데이터수집_yk.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victory_point 승소요지
# case_overview 사건 개요
# case_lawyer 변호사