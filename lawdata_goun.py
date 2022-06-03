# 법무법인 고운 성공사례 데이터 수집
from itertools import count
from urllib import response
from numpy import dtype
import requests
import urllib.request
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import traceback
from soupsieve import select
from PIL import Image
import pytesseract
import urllib3
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# 워크북 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['사건구분', '키워드/결과', '승소 요지', '사건 개요', '변호사'])

for case_num in range (1, 540): # uid = 1 ~ 539
    try:
        url = 'http://www.gounlaw.com/2019/information/civil_view.html?bmain=view&uid={}'.format(case_num)
        url = 'http://www.gounlaw.com/2019/information/civil_view.html?bmain=view&uid=358'
        # headers = {
        # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/605.1.15',
        # }
        response = requests.get(url) # allow_redirects=False
        rating_page = response.text
        soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
        case_num = 1
        if 'img' in str(soup):
            soup_img = soup.select('div.board-box')
            print(soup_img)
            url_img = soup_img[0].find('img')['src']
            print(url_img)
            fin_url_img = 'http://www.gounlaw.com/' + url_img
            print(fin_url_img)
            urllib.request.urlretrieve(str(fin_url_img), str(case_num) + '.jpg')
            '''
            urllib.error.HTTPError: HTTP Error 307: The HTTP server returned a redirect error that would lead to an infinite loop.        
            The last 30x error message was:
            Temporary Redirect - 서버 접근 제한
            '''
            
            im = Image.open(str(case_num) + '.jpg')
            text = pytesseract.image_to_string(im, lang='kor')
        
            if '변호사' or '담당변호사' in text:
                if '사건개요' in soup.select_one('div.board-box').get_text().strip():
                
                print('#### yes')
                case_division = ''
                case_keyword = re.sub('<p class="tit">|</p>','',str(soup.select('#contents > div.page-section > div > table > tbody > tr:nth-child(1) > th > p.tit')))
                print(case_keyword)
                case_tag = soup.select_one('div.board-box').get_text().strip()
                print(case_tag)
                case_content = re.split('사건개요|대응전략', case_tag)
                print(case_content)
                # case_victorypoint = re.sub(']|\xa0|[결과]|[','',case_content[2])
                case_victorypoint = case_content[2].strip()
                print(case_victorypoint)
                # case_overview = re.sub('</span>|<p class="md_p">|<br>|</br></p>|</div>|<div class="middle_txt">|<br/>','',case_content[1])
                case_overview = case_content[1]
                print(case_overview)
                lawyer_index_num = text.find('담당변호사')
                case_lawyer = text[lawyer_index_num+6:lawyer_index_num+9]
                row = [case_division, case_keyword, case_victorypoint, case_overview, case_lawyer]
                ws.append(row)
                print(row)
        else:
            pass
        
    except:
        print('.')
        
        
wb.save('고운_test.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victorypoint 승소요지 
# case_overview 사건개요
# case_lawyer 변호사

#########################################################이미지 파일 접근 불가##############################################################