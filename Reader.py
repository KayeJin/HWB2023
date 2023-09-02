import os
import docx

Img = ['jpg', 'JPG', 'png', 'PNG', 'gif',  'GIF', 'bmp', 'BMP', 'tif', 'TIF', 'tiff', 'TIFF']
Office = ['ppt', 'xlsx', 'docx', 'doc'] 
Wps = ['dps', 'wps', 'et']
Win = ['hiv', 'sam', 'system']
Txt = ['txt']
Eml = ['eml'] #邮件
class Reader:

    def __init__(self, src: str) -> None:
        self.file_list = []
        self.img_list = []
        self.office_list = []
        self.txt_list = []
        self.wps_list = []
        self.win_list = []
        self.code_list= []
        self.src = src

    def file_reader(self, src: str): 
        for root, dirs, files in os.walk(src):
            # print("root_dir: ", root) #当前目录路径
            # print("sub_dirs: ", dirs) #当前路径下所有子目录
            # print('files: ', files) #当前路径下所有非目录子文件
            for file in files:
                self.file_list.append(file)
        for file in self.file_list:
            if len(file.split('.')) == 2:
                if file.split('.')[1] in Img:           #image
                    self.img_list.append(file)
                    # self.file_list.remove(file)
                elif file.split('.')[1] in Office:      #office
                    self.office_list.append(file)
                elif file.split('.')[1] in Wps:         #wps
                    self.wps_list.append(file)
                elif file.split('.')[1] in Win:         #windows
                    self.win_list.append(file)
            # elif file.split('.')[1] in Code:
                elif file.split('.')[1] in Txt:         #txt
                    self.txt_list.append(file)
            else:                                       #linux文件、Win没有后缀
                if file in Win:
                    self.win_list.append(file)
                
if __name__ == '__main__':
    fr = Reader()
    fr.file_reader(u'../赛题材料')
    # fr.image_reader()
    # fr.office_reader()
    print(fr.file_list)
    print(fr.img_list)
    print(fr.office_list)
    print(fr.txt_list)
    print(fr.wps_list)
    print(fr.win_list)
