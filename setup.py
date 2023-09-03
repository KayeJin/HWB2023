#解压缩
#doc/ppt ---> docx/pptx
import os, glob
import subprocess
from multiprocessing.dummy import Pool
import Reader

def file_reader(src: str, files: []):
    print(files)
    for file in files:
        if file.split('.')[1] in ['doc', 'ppt', 'wps', 'dps', 'et']:
            x = src + '/'
            sudoPassword = 'asdfghjkl'
            dic = {'doc': 'docx', 'ppt': 'pptx', 'wps': 'docx', 'dps': 'pptx', 'et': 'xlsx'}
            command = 'libreoffice --headless --convert-to ' + dic[file.split('.')[1]]+' '+ x + file + ' --outdir '+ x
            os.system('echo %s | sudo -S %s' % (sudoPassword,command))
                # subprocess.Popen('sudo -S', shell = True, stdout=subprocess.PIPE)
                # subprocess.Popen(sudoPassword, shell=True, stdout=subprocess.PIPE)
                # subprocess.Popen(command, shell=True, stdout =subprocess.PIPE)

if __name__ == '__main__':
    R = Reader.Reader(u'../赛题材料/wps')
    R.file_reader()
    file_reader(u'../赛题材料/wps', R.wps_list)
    
    ###问题：1. centos下需要sudo ----> os.popen实现
    ###      2. 找不到文件路径