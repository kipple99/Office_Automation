# 이미지(jpg, png...)파일 -> text 변환시켜주는 모듈
# pytesseract
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# 설치한 뒤 기본 경로

im = Image.open('test_ehyun1.jpg')

text = pytesseract.image_to_string(im, lang='kor')

print(text)
text.index('담당변호사 ')
text[232:235]