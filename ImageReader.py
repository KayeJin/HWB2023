### 从图片提取信息

from PIL import Image
from pytesseract import pytesseract
import enum
# import cv2
import os, sys
import Reader

class OS(enum.Enum):
    Mac = 0
    Windows = 1
    Linux = 2

class Languages(enum.Enum):
    ENG = 'eng'
    CHN = 'chi_sim'
    ENG_CHN = 'eng+chi_sim'

Img = ['.jpg', '.JPG', '.png', '.PNG', '.gif',  '.GIF', '.bmp', '.BMP', '.tif', '.TIF', '.tiff', '.TIFF']

class ImageReader: #从所有文件夹中读取所有图片文件

    def __init__(self,  src: str, img_list: []) -> None:
        self.src = src
        self.img_list = img_list

        # if os == OS.Linux:
        #     print('Running on Linux\n')

        # if os == OS.Windows:
        #     Windows_path = r'path:teseract.exe'
        #     pytesseract.tesseract_cmd = Windows_path
        #     print('Running on Windows\n')

        # if os == OS.Mac:
        #     print('Running on Mac\n')

    def extract_text(self, image: str, lang: Languages) -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, lang=lang.value)
        return extracted_text

    def save(self) -> str:
        res = []
        for img in self.img_list:
            text = self.extract_text(self.src+'/'+img, lang=Languages.ENG)
            res.append(text)
        with open("../image_text", 'w') as f:
            for i in res:
                f.write(i)

if __name__ == '__main__':
    IR = Reader.Reader('../赛题材料')
    IR.file_reader(IR.src)
    ir = ImageReader(OS.Linux, IR.src, IR.img_list)
    ir.save()
