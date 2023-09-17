# -*- coding: utf-8 -*-
#解压缩
import os, glob
import Decompress  
import Reader, WordReader, ExcelReader, PPtReader, ImageReader
# from ImageReader import OS
import sys
from pathlib import Path


if __name__ == '__main__':
    compress_src = ''
    try:
        compress_src = sys.argv[1] #输入压缩包
        print(compress_src)
    except Exception as e:
        print(sys.argv)
        print(e)
    S = Decompress.SaveFile(compress_src, '')
    S.extractFile()
    S.changeFormat()
    print(S.decom_src)
    Path('../IMAGE').mkdir(parents=True,exist_ok=True) #创建文件夹

    R = Reader.Reader(S.decom_src)
    R.file_reader()
    wR = WordReader.WordReader(S.decom_src, R.office_list)
    wR.getText()
    pR = PPtReader.PPtReader(S.decom_src, R.office_list)
    pR.getText()
    eR = ExcelReader.ExcelReader(S.decom_src, R.office_list)
    eR.getText()
    files = os.listdir('../IMAGE/')
    print(type(files))
    for i in files:
        R.img_list.append('../IMAGE/'+i) #设好路径
    print(len(R.img_list))
    
    # iR = ImageReader.ImageReader(R.src, R.img_list)
    # iR.save()

                

 