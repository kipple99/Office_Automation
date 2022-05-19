import pytesseract
import cv2
import matplotlib.pyplot as plt

path = 'test_picture.JPG'
image = cv2.imread(path)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BAYER_BG2RGB)

text = pytesseract.image_to_string(rgb_image, lang = 'kor+eng')
print(text)