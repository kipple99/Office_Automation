from urllib import response
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import traceback

from soupsieve import select

# 워크북 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['사건구분', '키워드/결과', '승소 요지/사건 개요', '변호사'])

for case_num in range(1, 7416): # 1 ~ 7415까지 크롤링
    try:
        url = 'https://www.minwho.kr/case/latest_case.html?bmain=view&uid={}'.format(case_num)
        url = 'https://www.minwho.kr/case/latest_case.html?bmain=view&uid=846'
        response = requests.get(url)
        rating_page = response.text
        soup = BeautifulSoup(rating_page, 'html.parser')            
        # test = soup.select_one('div.board-box').get_text().strip()
        # print(test)
        
        # test_1 = re.sub('  +', ' ', re.sub('[\n|\xa0]', ' ', test)).strip() # re.sub('  +') - 공백 2개 이상 제거
        # print(test_1)
        test = soup.select_one('p.bar_span').get_text().strip()
        test_1 = test.splitlines() # 줄바꿈 기호 기준으로 쪼개기
        print(test_1[1])
        
        if '승소' in soup.select_one('p.tit').get_text(): # 제목에 '승소'가 들어간 것만 작동
            case_tag = soup.select_one('p.bar_span').get_text().strip()
            case_tags = case_tags.splitlines() # 줄바꿈 기호 기준으로 쪼개기
            case_division = case_tags[0]
            case_keyword = soup.select_one('p.tit').get_text()
            case_victorypoint_overview_test = soup.select_one('div.board-box').get_text().strip()
            case_victorypoint_overview = re.sub('  +', ' ', re.sub('[\n|\xa0]', ' ', case_victorypoint_overview_test)).strip() # 공백 다 제거
            case_lawyer = case_tags[1]
            
        
    except:
            print('.')
            

wb.save('록션_데이터수집_민후.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victorypoint_overview 승소요지 / 사건개요
# case_lawyer 변호사