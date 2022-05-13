from urllib import response
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import re
import traceback

from soupsieve import select
from sqlalchemy import case

from urllib import response
import warnings
from logging.config import dictConfig
import logging
import inspect
import traceback
import os
import datetime


''' log '''
warnings.filterwarnings(action = 'ignore') 
filePath = os.path.dirname(os.path.abspath(__file__))
fileName = re.split('[.]', re.split('\\\\', inspect.getfile(inspect.currentframe()))[-1])[0]

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s --- %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '{}/logs/{}_{}.log'.format(filePath, fileName, re.sub('-', '', str(datetime.date.today()))),
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})

def log(msg):
    logging.info(msg)

 # 워크북 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()
ws.append(['사건구분', '키워드/결과', '승소 요지/사건 개요', '변호사'])

log('############ Program Start')

for case_num in range(1, 7416): # 1 ~ 7415까지 크롤링
    try:
        url = 'https://www.minwho.kr/case/latest_case.html?bmain=view&uid={}'.format(case_num)
        log('#### URL : {}'.format(url))
        response = requests.get(url)
        rating_page = response.text
        soup = BeautifulSoup(rating_page, 'html.parser')            
        test_keyword = str(soup.select_one('p.tit'))
        # test = soup.select_one('div.board-box').get_text().strip()
        # print(test)
        # test_1 = re.sub('  +', ' ', re.sub('[\n|\xa0]', ' ', test)).strip() # re.sub('  +') - 공백 2개 이상 제거
        # print(test_1)
        # test = soup.select_one('p.bar_span').get_text().strip()
        # test_1 = test.splitlines() # 줄바꿈 기호 기준으로 쪼개기
        # print(test_1[1])
        # print(test_keyword)
        
        if  '승소' in test_keyword: # 제목에 '승소'가 들어간 것만 작동
            log('######## 승소 O')
            case_tag = soup.select_one('p.bar_span').get_text().strip()
            case_tags = case_tag.splitlines() # 줄바꿈 기호 기준으로 쪼개기
            case_division = case_tags[0].replace('관련 업무분야 : ', '')
            case_keyword = soup.select_one('p.tit').get_text()
            case_victorypoint_overview_test = soup.select_one('div.board-box').get_text().strip()
            case_victorypoint_overview = re.sub('  +', ' ', re.sub('[\n|\xa0]', ' ', case_victorypoint_overview_test)).strip() # 공백 다 제거
            case_lawyer = case_tags[1]
            row = [case_division, case_keyword, case_victorypoint_overview, case_lawyer]
            ws.append(row)
        else:
            log('######## 승소 X')
    except:
        log('######## Error')
        log(traceback.format_exc())

wb.save('록션_데이터수집_민후.xlsx')

# case_division 사건 구분
# case_keyword 키워드
# case_victorypoint_overview 승소요지 / 사건개요
# case_lawyer 변호사