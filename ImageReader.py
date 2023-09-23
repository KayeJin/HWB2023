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
from PIL import Image, ImageEnhance
import shutil
from pathlib import Path
from paddleocr import PPStructure,draw_structure_result,save_structure_res, PaddleOCR
from bs4 import BeautifulSoup
import pandas as pd
import logging


logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
logging.disable(logging.WARNING) 


os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
class Languages(enum.Enum):
    ENG = 'eng'
    CHN = 'chi_sim'
    ENG_CHN = 'eng+chi_sim'

Img = ['jpg', 'JPG', 'jpeg' , 'JPEG' , 'png', 'PNG', 'gif',  'GIF', 'bmp', 'BMP', 'tif', 'TIF', 'tiff', 'TIFF']
Vector = ['wmf', 'WMF', 'svg', 'SVG', 'emf', 'EMF']
class ImageReader: #从所有文件夹中读取所有图片文件

    def __init__(self,  src: str, img_list: [], imgDir: str) -> None:
        self.src = src
        self.img_list = img_list
        self.ImageDir = imgDir
        self.img_path = 'IMAGE/'
        self.newImg_path = 'BINIMAGE/'
        Path("BINIMAGE/").mkdir(parents=True, exist_ok=True)
        Path("IDIR/").mkdir(parents=True, exist_ok=True)

    def extract_text(self, image: str) -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, 'eng+chi_sim')
        return extracted_text
    
    def extract_text_paddle(self, image:str):
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
        img_path = image
        result = ocr.ocr(img_path, cls=True)
        res = []
        for line in result:
            res.append(line)
        return res
    
    def extract_text_ppstucture(self, image:str):
        table_engine = PPStructure(show_log=False)
        res = []
        img_list = image
        img_path = image
        img = cv2.imread(img_path)
        result = table_engine(img) #一个图片对应一个列表中的字典
        # save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])
        c = 0
        for fleid in range(len(result)):
            type = result[fleid]['type']

            if type == 'table':
                text = result[fleid]['res']['html']
                if text == []:
                    continue
                soup = BeautifulSoup(text, 'html.parser')
                tables = soup.find_all('table')  # 查看当前html页面所有table 元素<可能含有多个>
                
                file_name = str(c)  + '.xlsx' #excel表格存储在dDIR中
                c += 1
                # ExcelWriter is the class for writing DataFrame objects into excel sheets.
                writer = pd.ExcelWriter(file_name, engine='xlsxwriter')  # Excel 写操作对象
                workbook = writer.book  # 创建工作簿
                for idx, table in enumerate(tables):
                    table_title = 'Table-' + str(idx)
                    # Read HTML tables into a list of DataFrame objects.
                    df_table = pd.read_html(str(table), header=0, flavor='bs4')[0]
                    df_table.dropna(how='all', inplace=True)  # 当一整行都是nan时，去掉该行
                    df_table.to_excel(writer, index=False, sheet_name=table_title)  # 将df对象转换成Excel表格

                    worksheet = writer.sheets[table_title] # 添加该子表
                    # 对工作簿添加样式
                    header_fmt = workbook.add_format({'font_size': 14, 'bold': True, 'fg_color': '#D7E4BC', 'border': 1})
                    # 对子表的第一行的字段设置样式
                    for col_num, value in enumerate(df_table.columns.values):
                        worksheet.write(0, col_num, value, header_fmt)
                    # 设置工作簿列宽
                    worksheet.set_column('A:Z', 25)
                # # Close the Pandas Excel writer and output the Excel file.
                writer.close()

            elif type != 'table':
                text = result[fleid]['res'] #还是个列表
                if text != []:
                    X_point = text[0]['text_region'][0][1]#左上像素点的行坐标
                    Y_point = text[0]['text_region'][0][0]#左上像素点的列坐标
                    pre_X_point = X_point
                    pre_Y_point = Y_point
                    for dic in text:
                        X_point = dic['text_region'][0][1]
                        Y_point = dic['text_region'][0][0]#右上
                        if X_point > (pre_X_point + 15)   :
                            res.append("\n") #换行
                        else:
                            res.append(" ")
                        res.append(dic['text'])
                        pre_X_point = X_point
                        pre_Y_point = Y_point
        return res


    def pre_processing(self) -> None:
        filename = self.img_list
        img_list = []
        Path('IDIR/').mkdir(parents=True, exist_ok=True)
        for img in filename:
            if img.split('.')[-1] not in Img: #将矢量图转为位图
                command = f"libreoffice --headless --convert-to png {img} --outdir {self.img_path}"
                os.system(command)
                os.remove(img)

        for img_name in filename:
            newname = 'IDIR/' + img_name.split('/')[-1] #对比度增强图片放到的位置
            img = Image.open(img_name)
            #增强对比度
            contrast = ImageEnhance.Contrast(img.convert('RGB'))
            sharpness = ImageEnhance.Sharpness(img.convert('RGB'))
            img = sharpness.enhance(1.5)
            img_list.append(newname)
            img.save(newname)
        filename = img_list
        for img in filename:
            img_name = img
            name = os.path.splitext(img.split('/')[-1])[0]
            newFileName = self.newImg_path + name + ".bmp"
            im = cv2.imread(img)

            grayImg = cv2.cvtColor(im,  cv2.COLOR_BGR2GRAY) #灰度化 https://blog.51cto.com/u_15506603/6534086
            ret, thresh = cv2.threshold(grayImg, 0 ,255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) #二值化
            cv2.imwrite(newFileName, thresh)

    def save(self) -> str:
        res = []
        img = []

        self.pre_processing()
        newimg = os.listdir(self.newImg_path)
        for i in newimg:
            img.append(self.newImg_path+i)

        before = time.time()
        pool = Pool(processes=3)
        res = pool.map_async(self.extract_text, img)
        # res = pool.map_async(self.extract_text_ppstucture, img)
        # res = pool.map_async(self.extract_text_paddle, img)
        pool.close()
        pool.join()
        res = res.get()
        after = time.time()
        print("1 : ", after-before)




        # with open("fileDIR/image_text_Tess", 'w') as f:
            # for i in res:
            #     f.write(i)
        # with open("../image_text55_PPStur", 'w') as f:
        #     for line in res:
        #         for i in line:
        #             f.write(i)
        with open("fileDIR/image_text.txt", 'w') as f:
            for line in res:
                for i in line:
                    f.write(str(i))
        # with open("../time.txt", "w") as f:
        #     for i in ocrtime:
        #         f.write(i + "\n")

if __name__ == '__main__':
    IR = Reader.Reader('IMAGE/')
    IR.file_reader()
    ir = ImageReader( IR.src, IR.img_list, 'IMAGE/')
    
    ir.save()
