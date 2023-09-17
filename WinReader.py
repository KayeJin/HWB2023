# -*- coding: utf-8 -*-

import os
import Reader
import subprocess
import encodings.idna
# from impacket import secretsdump

class WinReader:

    def __init__(self, src: str, win_list: []) -> None :
        self.src = src
        self.win_list = win_list
        self.win_dict = {}
    def getText(self):
        res = []
        for file in self.win_list:
            #提取sam文件
            if 'sam' in file.split('%')[-1] :
                self.win_dict[file] = ''

        for file in self.win_list:
            if 'system' in file.split('%')[-1] :
                for key in self.win_dict:
                    if file[0: -len(file.split('%')[-1])] == key[0: -len(key.split('%')[-1])]:
                        # print(file[0: -len(file.split('%')[-1])] )
                        self.win_dict[key] = file

        for key, value in self.win_dict.items():

            # s = "secretsdump.py -sam " + self.src + key + " -system " + self.src + value + " LOCAL"
            s = "secretsdump.py -sam " +  key + " -system " +  value + " LOCAL"
            res.append(subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT))

        with open("../Win_test22", "w") as f:
            for i in res:  
                for line in i.stdout.readlines():
                    f.write(str(line) + "\n")
            

if __name__ == "__main__":
    R = Reader.Reader("dDIR/")
    R.file_reader()
    wR = WinReader(R.src, R.win_list)
    # print(R.win_list)
    
    wR.getText()