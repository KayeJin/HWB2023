### 从图片提取信息

from PIL import Image
from pytesseract import pytesseract
# from threading import Timer
import time
import enum
import cv2
import os, sys
import Reader
from multiprocessing import Pool,cpu_count
import numpy as np 
from PIL import Image
import shutil
from pathlib import Path



class Languages(enum.Enum):
    ENG = 'eng'
    CHN = 'chi_sim'
    ENG_CHN = 'eng+chi_sim'

Img = ['.jpg', '.JPG', '.png', '.PNG', '.gif',  '.GIF', '.bmp', '.BMP', '.tif', '.TIF', '.tiff', '.TIFF']

class ImageReader: #从所有文件夹中读取所有图片文件

    def __init__(self,  src: str, img_list: []) -> None:
        self.src = src
        self.img_list = img_list
        self.img_path = '../IMAGE/'
        self.newImg_path = '../BINIMAGE/'
        # filename = os.listdir(self.img_path) #图像名列表
        Path("../BINIMAGE").mkdir(parents=True, exist_ok=True)

    def extract_text(self, image: str) -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, 'eng+chi_sim')
        return extracted_text

    def pre_processing(self) -> None:
        # filename = os.listdir(self.img_path) #图像名列
        filename = self.img_list
        for img in filename:
            # print(img.split('/')[-1])
            name = os.path.splitext(img.split('/')[-1])[0]
            newFileName = self.newImg_path + name + ".bmp"
            im = cv2.imread(img)
            grayImg = cv2.cvtColor(im,  cv2.COLOR_BGR2GRAY) #灰度化 https://blog.51cto.com/u_15506603/6534086
            ret, thresh = cv2.threshold(grayImg, 0 ,255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) #二值化
            cv2.imwrite(newFileName, thresh)

    def save(self) -> str:
        res = []
        img = []
        # img = self.img_list
        self.pre_processing()
        newimg = os.listdir(self.newImg_path)
        for i in newimg:
            img.append(self.newImg_path+i)
        before = time.time()
        pool = Pool(processes=3)
        res = pool.map_async(self.extract_text, img)
        pool.close()
        pool.join()
        res = res.get()
        after = time.time()
        print("1 : ", after-before)

        with open("../image_text44", 'w') as f:
            for i in res:
                f.write(i)

if __name__ == '__main__':
    IR = Reader.Reader('../IMAGE/')
    IR.file_reader()
    # print(IR.img_list)

    ir = ImageReader( IR.src, IR.img_list)
    
    ir.save()
