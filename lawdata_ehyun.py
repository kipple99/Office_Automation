# 법무법인 이현 성공사례 데이터 수집
from itertools import count
from urllib import response
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

for case_num in range(1, 963): # range(1, 963)
    try:
        url = 'https://ehyun.co.kr/bbs/board.php?bo_table=success&wr_id={}'.format(case_num)
        response = requests.get(url)
        rating_page = response.text
        soup = BeautifulSoup(rating_page, 'html.parser')
        
        if 'img' in str(soup):
            soup_img = soup.select('div.results-contents')
            url_img = soup_img[0].find('img')['src'] 
            urllib.request.urlretrieve(url_img, str(case_num) + '.jpg')
            
            im = Image.open(str(case_num) + '.jpg')
            text = pytesseract.image_to_string(im, lang='kor')
        
            if '담당변호사' in text:
                print('#### yes')
                case_division = ''
                case_keyword = soup.select_one('h1').get_text() 
                case_tag = soup.select('div.middle_txt')
                case_content = re.split('<span class="md_span">', str(case_tag))
                case_victorypoint = re.sub('</span>|<p class="md_p">|<br/>|<br/>|</div>|<div class="middle_txt">|</p>','',case_content[2])
                case_overview = re.sub('</span>|<p class="md_p">|<br>|</br></p>|</div>|<div class="middle_txt">|<br/>','',case_content[1])
                lawyer_index_num = text.find('담당변호사')
                case_lawyer = text[lawyer_index_num+6:lawyer_index_num+9]
                row = [case_division, case_keyword, case_victorypoint, case_overview, case_lawyer]
                ws.append(row)
                print(row)
        else:
            pass
        
    except:
        print('.')
        
        
wb.save('이현_test.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victorypoint 승소요지 
# case_overview 사건개요
# case_lawyer 변호사