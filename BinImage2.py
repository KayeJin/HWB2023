import cv2
import os 
import numpy as np 
from PIL import Image
import shutil
from pathlib import Path
import imutils

filepath = '../IMAGE/'
filename = os.listdir(filepath) #图像名列表
Path("../BINIMAGE4").mkdir(parents=True, exist_ok=True)
new_dir = '../BINIMAGE4/'
for img in filename:
    name = os.path.splitext(img)[0]
    newFileName = new_dir+name + ".bmp"
    img = filepath+img
    im = cv2.imread(img)
    # rows, cols = im.shape[:2]
    # if rows < 485:
    #     im = cv2.resize(im,(485,485))
    
    grayImg = cv2.cvtColor(im,  cv2.COLOR_BGR2GRAY) #灰度化 https://blog.51cto.com/u_15506603/6534086
    ret, thresh = cv2.threshold(grayImg, 100 ,255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) #二值化
    cv2.imwrite(newFileName, thresh)
    # kernel = np.ones((7,1),np.uint8)
    # dilation = cv2.dilate(thresh,kernel,iterations=1) #图像膨胀
    # cnts = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)

    # for c in cnts: #外接矩阵
    #     x,y,w,h = cv2.boundingRect(c)
    #     cv2.rectangle(thresh, (x,y) ,(x+w,y+h), (255,0,0), 1)
    #     if(h < 15):
    #         cv2.fillPoly(thresh, pts=[c], color=(0)) #过滤字符，标点符号去掉

    # # for i, c in enumerate(cnts):
    # #     x,y,w,h=cv2.boundingRect(c)
    # #分割
    # char_list = []
    # for c in cnts:
    #     x,y,w,h = cv2.boundingRect(c)
    #     if h < 15:
    #         continue
    #     cropImg = thresh[y:y+h, x:x+w]
    #     char_list.append((x,cropImg))
    # # print(char_list)
    # for ch in char_list:
    #     cv2.imwrite(newFileName, ch[1]) #写入文件

