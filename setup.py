#解压缩
#doc/ppt ---> docx/pptx
import os, glob
import subprocess
from multiprocessing.dummy import Pool

def file_reader(src: str):
    for roots, dirs, files in os.walk(src):
        for file in files:
            if file[-3:] == 'doc':
                x = src + '/office/'
                sudoPassword = 'asdfghjkl'
                command = 'libreoffice --headless --convert-to docx ' + x + file + ' --outdir '+ x
                os.system('echo %s | sudo -S %s' % (sudoPassword,command))
                # subprocess.Popen('sudo -S', shell = True, stdout=subprocess.PIPE)
                # subprocess.Popen(sudoPassword, shell=True, stdout=subprocess.PIPE)
                # subprocess.Popen(command, shell=True, stdout =subprocess.PIPE)

if __name__ == '__main__':
    file_reader(u'../赛题材料')
    
    ###问题：1. centos下需要sudo ----> os.popen实现
    ###      2. 找不到文件路径