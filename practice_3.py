import requests
from bs4 import BeautifulSoup as bs
import telegram
import time
import pandas as pd

# 사건구분 / 키워드, 결과 / 승소요지 / 사건 개요 / 변호사 를 담을 빈 리스트 선언
case_division = [] # 사건 구분
case_keyword = [] # 키워드
case_victory_point = [] # 승소요지
case_overview = [] # 사건 개요
# case_lawyer = [] #사건 변호사 (이미지)


#try except 문으로 예외처리 나누기
# for문을 이용해서 원하는 페이지에 접근, 정보 추출 후 리스트에 담기
for page_num in range(14): 
    for i in range(778):
        # range를 이용하면 0부터 인덱스가 시작되므로 page_num에 1을 더해준 url을 이용
        # url = f'http://www.lawfirmak.com/bk/?page_id=24194&uid={i}&mod=document&pageid={page_num+1}'
        url = 'http://anlab.co.kr/%ec%97%85%eb%ac%b4%ec%82%ac%eb%a1%80/?pageid=11&mod=document&uid=2660'
        
        # html 정보 받아와서 파싱
        response = requests.get(url)
        soup = bs(response.text , 'html.parser')

        # selector로 페이지 내의 원하는 정보 가져오기
        html_division = soup.select('div.content-view')
        
        ## yjjo
        html_division = list(map(str, list(soup.select('div.content-view>p'))))
        
        idx_list = []
        for idx, val in enumerate(html_division):
            if '<p><img' in val or val == '<p>\xa0</p>':
                idx_list.append(idx)
        # [1], [2]가 image일때 len(idx_list) = 4
        
        if len(idx_list) == 4:
            case = ' '.join(html_division[idx_list[1] + 1 : idx_list[2]])
            win_keyword = ' '.join(html_division[idx_list[2] + 1 : idx_list[3]])
            
            case = re.sub('<p>|</p>', '', case)
            win_keyword = re.sub('<p>|</p>', '', win_keyword)
        
        elif len(idx_list) == 3:
            case = ' '.join(html_division[idx_list[0] + 1 : idx_list[2]])
            win_keyword = ' '.join(html_division[idx_list[1] + 1 : idx_list[2]])
            
            case = re.sub('<p>|</p>', '', case)
            win_keyword = re.sub('<p>|</p>', '', win_keyword)
        
        
        
        
        
        html_keyword = soup.select('div.kboard-title')
        html_victory_point = soup.select()
        html_overview = soup.select()
        #html_lawyer = soup.select()

        # 텍스트만 추출
        for i in html_division:
            case_division.append(i.get_text())

        for i in html_keyword:
            case_keyword.append(i.get_text())

# zip 모듈을 이용해서 list를 묶어주기        
list_sum = list(zip(case_division, case_keyword, case_victory_point, case_overview))


# 데이터프레임의 첫행에 들어갈 컬럼명
col = ['사건구분', '키워드, 결과', '승소요지', '사건 개요', '변호사']

# pandas 데이터 프레임 형태로 가공
df = pd.DataFrame(list_sum, columns=col)

# 엑셀에 저장
df.to_excel('록션 데이터 수집_AnLab.xlsx')




# 조용준
import re

text = case_keyword[0]

text_list = re.split('\n', text)

text_list2 = list(map(lambda x : None if x == '\xa0' else x, text_list))

text_list3 = list(filter(None, text_list2))

idx_list = []
for idx, val in enumerate(text_list3):
    if '1. ' in val or '2. ' in val or '3. ' in val or '4. ' in val:
        idx_list.append(idx)
        
' '.join(text_list3[idx_list[0] + 1 : idx_list[1]])
' '.join(text_list3[idx_list[1] + 1 : idx_list[2]])
' '.join(text_list3[idx_list[2] + 1 : idx_list[3]])