# -*- coding: utf-8 -*-
#解压缩
import os, glob
import Decompress  
import Reader, WordReader, ExcelReader, PPtReader, ImageReader, EmlReader, sensitive

import sys, time, shutil
from pathlib import Path


if __name__ == '__main__':
    compress_src = ''
    try:
        compress_src = sys.argv[1] #输入压缩包
        # print(compress_src)
    except Exception as e:
        # print(sys.argv)
        print("请输入压缩包！")
        exit()
    start = time.time()
    Path('dDIR/').mkdir(parents=True,exist_ok=True) #文件统一存放在dDIR中
    Path('fileDIR/').mkdir(parents=True,exist_ok=True)
    print("开始解压缩:")
    S = Decompress.SaveFile(compress_src, 'dDIR/')
    S.extractFile()
    S.changeFormat()
    print(S.decom_src)
    Path('IMAGE/').mkdir(parents=True,exist_ok=True) #图片统一放在IMAGE中
    Path("BINIMAGE/").mkdir(parents=True, exist_ok=True) #预处理后的图片放在BINIMAGR中
    print("解压缩结束: \n\n")
    print("开始内容提取模块：")
    R = Reader.Reader(S.decom_src)
    R.file_reader()
    ER = EmlReader.EmlReader(R.eml_list, S.decom_src, "IMAGE/")
    ER.emlAnayalyse()
    wR = WordReader.WordReader(S.decom_src, R.office_list, "IMAGE/")
    wR.getText()
    pR = PPtReader.PPtReader(S.decom_src, R.office_list, "IMAGE/")
    pR.getText()
    eR = ExcelReader.ExcelReader(S.decom_src, R.office_list)
    eR.getText()
    files = os.listdir('IMAGE/')
    # print(type(files))
    for i in files:
        R.img_list.append('IMAGE/'+i) #设好路径
    # print(len(R.img_list))
    
    iR = ImageReader.ImageReader(R.src, R.img_list, "IMAGE/")
    iR.save()
    end = time.time()
    print("total time : ", end-start)
    print("内容提取模块结束：\n\n")
    print("开始敏感信息提取：")
    sensitive.extract_file("fileDIR/")
    print("敏感信息提取结束：")
    shutil.rmtree('IMAGE/')
    shutil.rmtree('BINIMAGE/')
    shutil.rmtree('IDIR/')

                

 