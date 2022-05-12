import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import traceback

# 워크북 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['사건구분', '키워드/결과', '승소 요지', '사건 개요', '변호사'])

n = 267838
for page in range(151, 201): # 151 ~ 200 page까지 크롤링
    n2 = 0
    for case_num in range(n, 269890): # url = v value 267838 ~ 269889(267838 ~ 269788) 까지
        try:
            # 웹 페이지 가져와서 BeautifulSoup 생성
            url = "http://www.yklaw.net/deteg/success/?&page={}&v={}".format(page, case_num)

            response = requests.get(url)
            rating_page = response.text
            soup = BeautifulSoup(rating_page, 'html.parser')
            #soup.select('span')[11]

            if '사건담당변호사' in str(soup.select('p')[-1]):
                
                case_division = ''
                case_keyword = re.sub('<span>|</span>|<span class="category">', '', str(soup.select('span')[11]) + ' ' + str(soup.select('span')[12])).strip()
                case_victory_point = re.sub('<p>|</p>|\n', '', str(soup.select('p')[3])).strip()
                case_overview = re.sub('<p>|</p>|\n', '', str(soup.select('p')[1])).strip()
                case_lawyer = re.sub('<span>|</span>|<span class="name">', '', str(soup.select('span.name')[0])+ ' ' + str(soup.select('span.name')[1])).strip()
                row = [case_division, case_keyword, case_victory_point, case_overview, case_lawyer]
                ws.append(row)
                print(row)
                n = case_num + 1
                n2 += 1
                if n2 == 15:
                    break # continue 메소드를 사용해도 끊김
                    print(traceback.format_exc())
        except:
            print('.')
            

wb.save('록션_데이터수집_yk_6.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victory_point 승소요지
# case_overview 사건 개요
# case_lawyer 변호사