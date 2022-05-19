# 태림 법률 사무소 성공사례 데이터 수집
from urllib import response
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import traceback
from soupsieve import select
from sympy import primefactors


# 워크북 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['사건구분', '키워드/결과', '승소 요지/사건 개요', '변호사'])

for case_num in range(1517, 2390):
    try:
        url = 'https://www.tll.co.kr/html/dh_board/views/{}/?&search_value=%ED%83%9C%EB%A6%BC%EC%9D%98%20%EC%A1%B0%EB%A0%A5'.format(case_num)
        response = requests.get(url)
        rating_page = response.text
        soup = BeautifulSoup(rating_page, 'html.parser')
        case_division = ''
        case_keyword = soup.select_one('h1').get_text()
        
        case_tag = soup.select_one('div.content').get_text().strip()
        case_tags = case_tag.replace('\n','')
        print(case_tags)
        case_content = re.split('1.|2. 태림의 조력', case_tags)
        
        case_victorypoint = case_content[2]
        case_overview = case_content[1]
        case_lawyer = re.sub('<h1>|<font style="font-size: .8em; font-weight: 400; color: #89898e;">|</font>|</h1>|[|]','',str(soup.select('div.name_card_txt > h1')))
        row = [case_division, case_keyword, case_victorypoint, case_overview, case_lawyer]
        ws.append(row)
        print(row)
        
        
    except:
        print('.')
        
        
wb.save('록션 데이터수집_법률사무소_태림.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victorypoint 승소요지 
# case_overview 사건개요
# case_lawyer 변호사