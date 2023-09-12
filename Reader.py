import os
import docx
import shutil

Img = ['jpg', 'JPG', 'png', 'PNG', 'gif',  'GIF', 'bmp', 'BMP', 'tif', 'TIF', 'tiff', 'TIFF']
Office = ['ppt', 'xlsx', 'docx', 'doc', 'pptx'] 
# Wps = ['dps', 'wps', 'et']
Win = ['hiv', 'sam', 'system']
# Txt = ['txt']
# Eml = ['eml'] #邮件

class Reader:

    def __init__(self, src: str) -> None:
        self.file_list = []
        self.readable_list = []
        self.unreadable_list = []
        self.img_list = []
        self.office_list = []
        self.wps_list = []
        self.win_list = []
        self.src = src
        self.count = 0

    def file_reader(self): 
        for root, dirs, files in os.walk(self.src):
            for file in files:
                self.file_list.append(file)
        for file in self.file_list:
            with open(self.src+file, "r", encoding='utf-8') as f:
                try:
                    f.read()
                    self.readable_list.append(file)
                except UnicodeDecodeError:
                    self.unreadable_list.append(file)

        if os.path.exists(r'../Readable_text'):
            os.remove(r'../Readable_text')
        with open('../Readable_text', "a", encoding='utf-8') as f:
            for file in self.readable_list:
                f.write(file + "\n")
                self.count += 1
                with open(self.src+file, "r", encoding='utf-8') as rf:
                    f.write(rf.read())

        for file in self.unreadable_list:
            if len(file.split('.')) >= 2:
                if file.split('.')[-1] in Img:           #image
                    self.img_list.append(file)
                elif file.split('.')[-1] in Office:      #office
                    self.office_list.append(file)
                # elif file.split('.')[-1] in Wps:         #wps
                #     self.wps_list.append(file)
                elif file.split('.')[-1] in Win:
                    self.win_list.append(file)         #windows #.hiv
            else:                                       #Win没有后缀
                if file.split('%')[-1] in Win:          #win
                    self.win_list.append(file)

if __name__ == '__main__':
    fr = Reader(u'dDIR/')
    fr.file_reader()
    print(len(fr.file_list),len(fr.readable_list) + len(fr.unreadable_list),len(fr.unreadable_list), len(fr.office_list)+len(fr.img_list)+len(fr.win_list))
    print(fr.count)
    # print(fr.file_list)
    # print(fr.img_list)
    # print(fr.office_list)
    # # print(fr.txt_list)
    # print(fr.wps_list)
    # print(fr.win_list)
