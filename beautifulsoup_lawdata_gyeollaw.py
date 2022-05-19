# 법률사무소 결 성공사례 데이터 수집

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

for case_num in range(1, 269): # uid 1 ~ 268까지 크롤링
    try:
        url = 'http://gyeollaw.com/success/detective.html?bmain=view&uid={}'.format(case_num)
        response = requests.get(url)
        rating_page = response.text
        soup = BeautifulSoup(rating_page, 'html.parser')
        
        case_division = ''
        case_keyword = soup.select_one('p.tit').get_text()
        
        case_tag = soup.select_one('div.board-box').get_text().strip()
        case_tags = case_tag.replace('\xa0','')
        case_tag_split = re.split('\n', case_tags)
        
        case_victorypoint = list(filter(None, case_tag_split))[1]
        case_overview = list(filter(None, case_tag_split))[0]
        case_lawyer = re.sub('</p>|<p class="member-list-name">', ' ',str(soup.select('p.member-list-name')))
        row = [case_division, case_keyword, case_victorypoint, case_overview, case_lawyer]
        ws.append(row)
        print(row)

        

    except:
        print('.')


wb.save('록션_데이터수집_법률사무소_결.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victorypoint 승소요지 
# case_overview 사건개요
# case_lawyer 변호사