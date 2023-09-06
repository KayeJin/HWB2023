# -*- coding: utf-8 -*-
#解压缩
#doc/ppt ---> docx/pptx
import os, glob
import subprocess
from multiprocessing.dummy import Pool
import Reader
import sys,shutil
import gzip, tarfile, zipfile, rarfile
import random

sys.path

class Decompress: #题目：单个压缩包

    # compressed_list = ['gz', 'tar', 'zip', 'rar'] #类变量

    def __init__(self, compress_src: str, decompress_src: str) -> None:
        self.com_src = compress_src #压缩文件     #实例变量
        self.decom_src = ""
        self.allFile = [] #文件
        self.compressed_list = ['gz', 'tar', 'zip', 'rar']
        if decompress_src == '' :
            self.decompression()
        else:
            self.decom_src = decompress_src
            
    def ungz(self, filename = []) -> str:
        if filename == []:
            filename = self.com_src
        file_name = filename[:-3] #去掉.gz
        gz_file = gzip.GzipFile(filename)
        with open(file_name, "wb+") as file:
            file.write(gz_file.read())
        return file_name

    def untar(self, filename = []) -> str:
        if filename == []:
            filename = self.com_src
        file_name = filename[:-4] #去掉.tar
        tar = tarfile.open(filename)
        if not os.path.isdir(file_name):
            os.mkdir(file_name)
        else:
            os.mkdir(file_name+"_tar")
            file_name = file_name+"_tar"
        tar.extractall(file_name) 
        tar.close()
        return file_name

    def unzip(self, filename = []) -> str :
        if filename == []:
            filename = self.com_src
        file_name = filename[:-4] #去掉.zip
        zip = zipfile.ZipFile(filename)
        if not os.path.isdir(file_name):
            os.mkdir(file_name)
        else:
            os.mkdir(file_name+"_zip")
            file_name = file_name+"_zip"
        zip.extractall(file_name)
        zip.close()
        return file_name

    def unrar(self, filename = []) -> str: #未测试，centos需要下载rar包
        if filename == []:
            filename = self.com_src
        file_name = filename[:-4]
        rar = rarfile.RarFile(filename)
        if not os.path.isdir(file_name):
            os.mkdir(file_name)
        else:
            os.mkdir(file_name+"_rar")
            file_name = file_name+"_rar"
        os.chdir(file_name)
        rar.extractall()
        rar.close()
        return file_name

    def saveFile(self, src: str):
        for roots, dirs, files in os.walk(src):
            for file in files:
                self.allFile.append(os.path.join(roots, file)) #记录子压缩包的文件

    def decompression(self, filename = []) -> None :
        if filename == []:
            filename = self.com_src
        suffix = filename.split('.')[-1]
        subfilename = ''
        if suffix in self.compressed_list:
            if suffix == 'gz':
                new_filename = self.ungz(filename) #查看是否有tar后缀
                # os.remove(filename)
                if new_filename.split('.')[-1] == 'tar':
                    subfilename = self.untar(new_filename)
            elif suffix == 'tar':
                subfilename = self.untar(filename)
            elif suffix == 'zip':
                subfilename = self.unzip(filename)
            elif suffix == 'rar':
                subfilename = self.unrar(filename)
        if self.decom_src == '':
            self.decom_src = subfilename
        self.saveFile(subfilename)

class SaveFile(Decompress):

    def __init__(self, compress_src: str, decompress_src: str) -> None:
        super(SaveFile, self).__init__(compress_src, decompress_src) #初始化父类

    def extractFile(self) -> None:
        for roots, dirs, files in os.walk(self.decom_src):   
            for file in files:
                if file.split('.')[-1] not in self.compressed_list:
                    if os.path.join(roots, file) not in self.allFile:
                        self.allFile.append(os.path.join(roots, file)) #相对路径
                else:  #子压缩文件
                    self.decompression(os.path.join(roots, file))
        
        with open("allFile.txt", "w") as f: #保存文件
            for i in self.allFile:
                if i.split(".")[-1] not in self.compressed_list:
                    f.write(i + '\n')

    def changeFormat(self): 
        outdir_path = "destinationDir/"
        if os.path.exists(outdir_path):
            shutil.rmtree(outdir_path)
        os.mkdir(outdir_path)
        files = self.allFile 
        FileList = []

        for file in self.allFile: 
            file1 = '1' + file.replace('/', '%').replace('$','xx').replace('~','xxx')
            FileList.append(outdir_path + file1)   #多级目录 ---> 单个目录
            shutil.copy2(file, outdir_path + file1)
        with open('allFile.txt', 'w') as f:
            for i in FileList:
                f.write(i + "\n")
        for file in FileList:
            if file.split('.')[-1] in ['doc', 'ppt', 'wps', 'dps', 'et']:
                dic = {'doc': 'docx', 'ppt': 'pptx', 'wps': 'docx', 'dps': 'pptx', 'et': 'xlsx'}
                print(file)
                
                command =f"soffice --headless --convert-to {dic[file.split('.')[-1]]}  {file} --outdir {outdir_path} "  ###需修改
                os.system(command)
                os.remove(file)
                # subprocess.run(command, shell= True)
                
                


if __name__ == '__main__':
    if os.path.exists('../赛题材料_zip/'):
        shutil.rmtree('../赛题材料_zip/')
    S = SaveFile(compress_src='',decompress_src='../赛题材料')
    # S.decompression()
    S.extractFile()
    S.changeFormat()
 