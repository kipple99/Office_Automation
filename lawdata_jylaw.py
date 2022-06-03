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

for case_num in range(1380, 1814): # range(1380, 1814)
    try:
        url = 'https://jylaw.kr/html/sub4_detail.jsp?sc_no={}'.format(case_num)
        # url = 'https://jylaw.kr/html/sub4_detail.jsp?sc_no=1667'
        response = requests.get(url)
        rating_page = response.text
        soup = BeautifulSoup(rating_page, 'html.parser')
        
        if 'img' in str(soup):
            soup_img = soup.select('div.d_imgbox')
            url_img = soup_img[0].find('img')['src'] 
            fin_url_img = 'https://jylaw.kr/' + url_img.replace('..','')
            # case_num = 1667
            urllib.request.urlretrieve(fin_url_img, str(case_num) + '.jpg')
            
            im = Image.open(str(case_num) + '.jpg')
            text = pytesseract.image_to_string(im, lang='kor')
          
            if '담당변호사' or '변호사' in text:
                print('#### yes')
                case_division = ''
                case_keyword_split = soup.select_one('div.detail_title').get_text().strip()
                case_keyword = ' '.join(case_keyword_split.split())
                print(case_keyword)
                
                case_tag = soup.select_one('div.d_textbox').get_text().strip()
                case_content = re.split('1. 사건 개요|2. 변호인의 조력|3. 결과', str(case_tag))
                # case_victorypoint = re.sub('','',case_content[2])
                case_victorypoint = case_content[2]
                case_overview = case_content[1]
                # case_overview = re.sub('','',case_content[1])
                lawyer_index_num = text.find('담당변호사')
                case_lawyer = text[lawyer_index_num+6:lawyer_index_num+9]
                row = [case_division, case_keyword, case_victorypoint, case_overview, case_lawyer]
                ws.append(row)
                print(row)
        else:
            pass
        
    except:
        print('.')
        
        
wb.save('jy_lawdata.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victorypoint 승소요지 
# case_overview 사건개요
# case_lawyer 변호사