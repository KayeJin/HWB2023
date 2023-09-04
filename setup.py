# -*- coding: utf-8 -*-
#解压缩
#doc/ppt ---> docx/pptx
import os, glob
import subprocess
from multiprocessing.dummy import Pool
import Reader
import sys
import gzip, tarfile, zipfile, rarfile
import sys
sys.path

class Decompress: #题目：单个压缩包

    # compressed_list = ['gz', 'tar', 'zip', 'rar'] #类变量

    def __init__(self, compress_src: str, decompress_src: str) -> None:
        self.com_src = compress_src #压缩文件      #实例变量
        self.decom_src = decompress_src #解压缩文件
        self.compressed_list = ['gz', 'tar', 'zip', 'rar']
        

    def ungz(self, filename = []) -> None:
        if filename == []:
            filename = self.com_src
        file_name = filename[:-3] #去掉.gz
        gz_file = gzip.GzipFile(filename)
        with open(file_name, "wb+") as file:
            file.write(gz_file.read())
        self.decom_src = file_name
        # return file_name

    def untar(self, filename = []) -> None:
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
        self.decom_src = file_name

    def unzip(self, filename = []) -> None :
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
        self.decom_src = file_name

    def unrar(self, filename = []) -> None: #未测试，centos需要下载rar包
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
        self.decom_src = file_name

    def decompression(self, filename = []) -> None :
        if filename == []:
            filename = self.com_src
        suffix = filename.split('.')[-1]
        if suffix in self.compressed_list:
            if suffix == 'gz':
                new_filename = self.ungz(filename) #查看是否有tar后缀
                # os.remove(filename)
                if new_filename.split('.')[-1] == 'tar':
                    self.untar(new_filename)
            elif suffix == 'tar':
                self.untar(filename)
            elif suffix == 'zip':
                self.unzip(filename)
            elif suffix == 'rar':
                self.unrar(filename)

class SaveFile(Decompress):

    def __init__(self, compress_src: str, decompress_src: str) -> None:
        self.allFile = []
        # self.src = decompress_src #第一层目录
        super(SaveFile, self).__init__(compress_src, decompress_src) #初始化父类


    def extractFile(self) -> None:
        for roots, dirs, files in os.walk(self.decom_src):
            print(self.decom_src)
            for file in files:
                if file.split('.')[-1] not in self.compressed_list:
                    self.allFile.append(os.path.join(roots, file)) #相对路径
                    print(os.path.join(roots, file))
                else:  #子压缩文件
                    print('\n&&&&&&&&&&&&&&&&&&&&&&& \n')
                    self.decompression(os.path.join(roots, file))
            # for dir in dirs:
            #     print(os.path.join(roots,dir))
        # print(self.allFile)

    def changeFormat(src: str, files: []):
        print(files)
        for file in files:
            if file.split('.')[-1] in ['doc', 'ppt', 'wps', 'dps', 'et']:
                x = src + '/'
                sudoPassword = 'asdfghjkl'
                dic = {'doc': 'docx', 'ppt': 'pptx', 'wps': 'docx', 'dps': 'pptx', 'et': 'xlsx'}
                command = 'libreoffice --headless --convert-to ' + dic[file.split('.')[-1]]+' '+ x + file + ' --outdir '+ x
                os.sysconf(command)
                # os.system('echo %s | sudo -S %s' % (sudoPassword,command))




if __name__ == '__main__':
    # filename = 'test.rar'
    # unrar(filename)


    S = SaveFile(compress_src=[],decompress_src='../赛题材料1')
    S.extractFile()
    # R = Reader.Reader(u'../赛题材料/wps')
    # R.file_reader()
    # file_reader(u'../赛题材料/wps', R.wps_list)
    
    ###问题：1. centos下需要sudo ----> os.popen实现
    ###      2. 找不到文件路径