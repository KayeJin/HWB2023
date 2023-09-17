import Reader
from docx import Document, ImagePart
from os.path import basename #返回文件名 https://www.runoob.com/python/python-os-path.html
import os, shutil
from pathlib import Path

class WordReader:

    def __init__(self, src: str, office_list: []) -> None:
        self.src = src
        self.office_list = office_list
        

    def getText(self):  #文本
        res_text = []
        res_img  = []
        img_name = []
        res_table = []
        for file in self.office_list:
            if file.split('.')[-1] == 'docx' :
                document = Document(self.src+'/'+file)
                tables = document.tables #表格集
                for paragraph in document.paragraphs:
                    res_text.append(paragraph.text+"\n")
                    imgs = paragraph._element.xpath('.//pic:pic') #获取所有图片
                    for img in imgs: #https://blog.csdn.net/qq_39147299/article/details/125544621
                        for img_id in img.xpath('.//a:blip/@r:embed'): #获取图片id
                            part = document.part.related_parts[img_id] #根据图片id获取对应的图片
                            if isinstance(part, ImagePart): #保存图片
                                res_img.append(part.blob)
                                img_name.append('../IMAGE/'+file+'_'+basename(part.partname))
                                # name = file +'_'+ basename(part.partname)
                                # name = '../IMAGE/' + name
                                # with open(name, "wb") as f:
                                #     print(basename(part.partname))
                                #     f.write(part.blob)
                tables = document.tables #表格集
                for table in document.tables:
                    cells = table._cells
                    cells_string = [cell.text for cell in cells]
                    res_table.append(cells_string)
                    print(cells_string) #待写入文件
                
        with open("../word_text", 'w') as f:
            for i in res_text:
                f.write(i)
            for i in res_table:
                f.write(i)
        Path('../IMAGE').mkdir(parents=True,exist_ok=True)
        c = 0
        for i in img_name:
            with open(i, "wb") as f:
                f.write(res_img[c])
            c += 1

    # def getTable(self): # https://blog.csdn.net/zhouz92/article/details/107179616
    #     for file in self.office_list:
    #         if file.split('.')[-1] == 'docx':
    #             document = Document(self.src+'/'+file)
    #             tables = document.tables #表格集
    #             for table in tables:
    #                 cells = table._cells
    #                 cells_string = [cell.text for cell in cells]
    #                 print(cells_string) #待写入文件

    # def getPicture(self) -> []:
    #     for file in self.office_list:
    #         print(file)
    #         if file.split('.')[-1] == 'docx' :
    #             document = Document(self.src+'/'+file)
    #             for paragraph in document.paragraphs:
    #                 res = []
    #                 imgs = paragraph._element.xpath('.//pic:pic') #获取所有图片
    #                 if not imgs:
    #                     return []
    #                 print(imgs)
    #                 for img in imgs: #https://blog.csdn.net/qq_39147299/article/details/125544621
    #                     for img_id in img.xpath('.//a:blip/@r:embed'): #获取图片id
    #                         print(img_id)
    #                         part = document.part.related_parts[img_id] #根据图片id获取对应的图片
    #                         if isinstance(part, ImagePart): #保存图片
    #                             name = file +'_'+ basename(part.partname)
    #                             name = '../IMAGE/' + name
    #                             with open(name, "wb") as f:
    #                                 print(basename(part.partname))
    #                                 f.write(part.blob)


if __name__ == '__main__':
    WR = Reader.Reader('dDIR/')
    WR.file_reader()
    print(WR.office_list)
    wr = WordReader("dDIR/", WR.office_list)
    wr.getText()
    # wr.getPicture()