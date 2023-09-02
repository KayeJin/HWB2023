#解压缩
#doc/ppt ---> docx/pptx
import os, glob
import subprocess
from multiprocessing.dummy import Pool
import Reader

def file_reader(src: str, files: []):
    for file in files:
        if file[-3:] in ['doc', 'ppt']:
            x = src + '/office/'
            sudoPassword = 'asdfghjkl'
            dic = {'doc': 'docx', 'ppt': 'pptx'}
            command = 'libreoffice --headless --convert-to ' + dic[file[-3:]]+' '+ x + file + ' --outdir '+ x
            os.system('echo %s | sudo -S %s' % (sudoPassword,command))
                # subprocess.Popen('sudo -S', shell = True, stdout=subprocess.PIPE)
                # subprocess.Popen(sudoPassword, shell=True, stdout=subprocess.PIPE)
                # subprocess.Popen(command, shell=True, stdout =subprocess.PIPE)

if __name__ == '__main__':
    R = Reader.Reader(u'../赛题材料/office')
    R.file_reader()
    file_reader(u'../赛题材料', R.office_list)
    
    ###问题：1. centos下需要sudo ----> os.popen实现
    ###      2. 找不到文件路径