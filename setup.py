# -*- coding: utf-8 -*-
#解压缩
import os, glob
import Decompress  
import Reader, WordReader, ExcelReader, PPtReader, ImageReader
from ImageReader import OS
import sys


if __name__ == '__main__':
    # compress_src = ''
    try:
        compress_src = sys.argv[1] #输入压缩包
    except Exception as e:
        print(sys.argv)
        print(e)
    S = Decompress.SaveFile(compress_src, "dDIR/")
    # S.extractFile()
    # S.changeFormat()
    print(S.decom_src)

    R = Reader.Reader(S.decom_src)
    R.file_reader()
    wR = WordReader.WordReader(S.decom_src, R.office_list)
    wR.getText()
    wR.getPicture()
    wR.getTable()
    pR = PPtReader.PPtReader(S.decom_src, R.office_list)
    pR.getText()
    pR.getPicture()
    pR.getTable()
    eR = ExcelReader.ExcelReader(S.decom_src, R.office_list)
    eR.getText()
    iR = ImageReader.ImageReader(R.src, R.img_list)
    iR.save()

                

 