from urllib import response
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['기간', '순위', '프로그램', '시청률'])

for year in range(2010, 2019):
    for month in range(1, 13):
        for weekIndex in range(0, 5):
            url = 'https://workey.codeit.kr/ratings/index?year={}&month={}&weekIndex={}'.format(year, month, weekIndex)
            response = requests.get(url)
            rating_page = response.text
            soup = BeautifulSoup(rating_page, 'html.parser')
            
            for tr_tag in soup.select('tr')[1:]:
                td_tags = tr_tag.select('td')
                period = '{}년 {}월 {}주차'.format(year, month, weekIndex + 1)
                row = [
                    period, 
                    td_tags[0].get_text(), # 순위
                    td_tags[1].get_text(), # 채널
                    td_tags[2].get_text(), # 시청률
                ]
                ws.append(row)
                
wb.save('SBS_데이터.xlsx')