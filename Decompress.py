# -*- coding: utf-8 -*-
#解压缩
#doc/ppt ---> docx/pptx
import os, glob
import subprocess
from multiprocessing.dummy import Pool
import Reader
import sys,shutil
import gzip, tarfile, zipfile, rarfile
from zipfile import ZipFile
import random
from pathlib import Path

# rarfile.UNRAR_TOOL="/usr/bin/unar"

sys.path

class Decompress: #题目：单个压缩包

    # compressed_list = ['gz', 'tar', 'zip', 'rar'] #类变量

    def __init__(self, compress_src: str, DestinationDir: str, decompress_src: str) -> None:
        self.com_src = compress_src #压缩文件     #实例变量
        self.decom_src = decompress_src #写死
        print("****", self.decom_src)
        # Path(self.decom_src).mkdir(parents=True, exist_ok=True)
        self.allFile = [] #文件
        self.compressed_list = ['gz', 'tar', 'zip', 'rar']
        if decompress_src == '' :
            self.decompression()
        else:
            self.decom_src = decompress_src

    def support_gbk(self, zip_file: ZipFile): #zip中文乱码问题
        name_to_info = zip_file.NameToInfo
        for name, info in name_to_info.copy().items():
            real_name = name.encode('cp437').decode('gbk')
            if real_name != name:
                info.filename = real_name
                del name_to_info[name]
                name_to_info[real_name] = info
        return zip_file

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
        Path(file_name).mkdir(parents=True, exist_ok=True)
        # if not os.path.isdir(file_name):
        #     os.mkdir(file_name)
        # else:
        #     os.mkdir(file_name+"_tar")
        #     file_name = file_name+"_tar"
        tar.extractall(file_name) 
        tar.close()
        return file_name

    def unzip(self, filename = []) -> str :
        if filename == []:
            filename = self.com_src
        file_name = filename[:-4] #去掉.zip
        if not os.path.isdir(file_name):
            os.mkdir(file_name)
        else:
            # os.mkdir(file_name+"_zip")
            file_name = file_name+"_zip"
            Path(file_name).mkdir(parents=True, exist_ok=True)
        with self.support_gbk(ZipFile(filename)) as zfp:
            zfp.extractall(file_name)
        return file_name

    def unrar(self, filename = []) -> str: #未测试，centos需要下载rar包
        if filename == []:
            filename = self.com_src
        file_name = filename[:-4]
        Path(file_name).mkdir(parents=True,exist_ok=True)
        os.system('rar x '+ filename +" " + file_name +" -Y")
        return file_name
        # rar = rarfile.RarFile(filename)
        # # if not os.path.isdir(file_name):
        # #     os.mkdir(file_name)
        # # else:
        # #     os.mkdir(file_name+"_rar")
        # #     file_name = file_name+"_rar"
        # Path(file_name).mkdir(parents=True, exist_ok=True)
        # with rarfile.RarFile(filename, 'r') as rf:
        #         rf.extractall(file_name)
        # # os.chdir(file_name)
        # # rar.extractall()
        # rar.close()

    def extract_rar_file(rar_filename, destination_folder):
        try:
            with rarfile.RarFile(rar_filename, 'r') as rf:
                rf.extractall(destination_folder)
            print(f"RAR文件 {rar_filename} 已解压到 {destination_folder}")
        except rarfile.RarCannotExec as e:
            print(f"无法执行RAR程序：{e}")
        except rarfile.RarNoFiles as e:
            print(f"RAR文件不包含任何文件：{e}")
        except Exception as e:
            print(f"解压RAR文件时发生错误：{e}")


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

    def __init__(self, compress_src: str, DestinationDir: str) -> None:
        super(SaveFile, self).__init__(compress_src, DestinationDir, '') #初始化父类
        self.outdir_path = DestinationDir
        Path(self.outdir_path).mkdir(parents=True,exist_ok=True)

    def extractFile(self) -> None:
        # self.decompression()
        print('_________extractFile________________')
        print(self.allFile)
        for roots, dirs, files in os.walk(self.decom_src):   
            for file in files:
                if file.split('.')[-1] not in self.compressed_list:
                    if os.path.join(roots, file) not in self.allFile:
                        self.allFile.append(os.path.join(roots, file)) #相对路径
                else:  #子压缩文件
                    self.decompression(os.path.join(roots, file))

    def changeFormat(self): 
        # outdir_path = "dDIR/"
        # if os.path.exists(outdir_path):
        #     shutil.rmtree(outdir_path)
        # os.mkdir(outdir_path)
        files = self.allFile 
        FileList = []
        print(self.allFile)
        with open('allFile.txt', 'w') as f:
            for i in self.allFile:
                f.write(i+"\n")

        for file in self.allFile:
            file1 = file[len(file.split('/')[0]) + len(file.split('/')[1]) + 1 : ]
            file1 = '1' + file1.replace('/', '%')
            FileList.append(self.outdir_path + file1)   #多级目录 ---> 单个目录
            shutil.copy2(file, self.outdir_path + file1)

        with open('allFile2.txt', 'w') as f:
            for i in FileList:
                f.write(i+"\n")
        self.decom_src = self.outdir_path
        # with open('allFile.txt', 'w') as f:
        #     for i in FileList:
        #         if i.split('.')[-1] not in self.compressed_list:
        #             f.write(i + "\n")
        for file in FileList:
            # print('soffice -- OK')
            if file.split('.')[-1] in ['doc', 'ppt', 'wps', 'dps', 'et']:
                dic = {'doc': 'docx', 'ppt': 'pptx', 'wps': 'docx', 'dps': 'pptx', 'et': 'xlsx'}
                command =f"soffice --headless --convert-to {dic[file.split('.')[-1]]}  {file} --outdir {self.outdir_path} "  ###需修改
                #java有包可以做转换工作
                os.system(command)
                os.remove(file)
        
                # subprocess.run(command, shell= True)
                
                


if __name__ == '__main__':
    if os.path.exists('../赛题材料_zip/'):
        shutil.rmtree('../赛题材料_zip/')
    S = SaveFile(compress_src='',decompress_src='../dDIR')
    # S.decompression()
    S.extractFile()
    S.changeFormat()
 