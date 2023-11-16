from flanker import mime, addresslib
import re,  time
from bs4 import BeautifulSoup
import pandas as pd
class EmlReader():
    
    def __init__(self, eml_list: [], src: str, Img_src: str) -> None:
        self.eml_list = eml_list
        self.src = src #存放多模态文件的地方
        self.Img_src = Img_src

    def HtmlParser(self, content, name): #获取html数据以及html中的表格
        name = name.split(".")[0]
        soup = BeautifulSoup(content, 'html.parser')
        tables = soup.find_all('table')  # 查看当前html页面所有table 元素<可能含有多个>
        
        file_name = name  + '.xlsx' #excel表格存储在dDIR中
        # ExcelWriter is the class for writing DataFrame objects into excel sheets.
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')  # Excel 写操作对象
        workbook = writer.book  # 创建工作簿
        for idx, table in enumerate(tables):
            table_title = 'Table-' + str(idx)
            # Read HTML tables into a list of DataFrame objects.
            df_table = pd.read_html(str(table), header=0, flavor='bs4')[0]
            df_table.dropna(how='all', inplace=True)  # 当一整行都是nan时，去掉该行
            # print(df_table)
            df_table.to_excel(writer, index=False, sheet_name=table_title)  # 将df对象转换成Excel表格

            worksheet = writer.sheets[table_title] # 添加该子表
            # 对工作簿添加样式
            header_fmt = workbook.add_format({'font_size': 14, 'bold': True, 'fg_color': '#D7E4BC', 'border': 1})
            # 对子表的第一行的字段设置样式
            for col_num, value in enumerate(df_table.columns.values):
                worksheet.write(0, col_num, value, header_fmt)
            # 设置工作簿列宽
            worksheet.set_column('A:Z', 25)
        # # Close the Pandas Excel writer and output the Excel file.
        writer.close()
        print('Export End!')
        return soup.get_text().replace("\n\n","\n").replace("     ","\n")


    def attachEml1(self, eml): #附件！
        for part in eml.parts:
            if not part.content_type.is_multipart():    
                name = part.detected_file_name
                name = str(name).split('\"')[0]  # 导出文件名 一定正确？
                with open(self.src+ name, 'wb') as annex:
                    annex.write(part.body)

    # 邮件正文
    def contentEml(self, eml):
        # 判断是否为单部分
        if eml.content_type.is_singlepart():
            eml_body = eml.body
        else:
            eml_body = ''
            for part in eml.parts:
                # 判断是否是多部分
                if part.content_type.is_multipart():
                    eml_body += self.contentEml(part)
                else:
                    if part.content_type.main == 'text':
                        eml_body = part.body
        return eml_body

    #邮件解析
    def emlAnayalyse(self):

        for eml_file in self.eml_list:
            # path = eml.split('.')[0] + '.txt'
            with open(eml_file, 'rb') as fhdl:
                raw_email = fhdl.read()
                eml = mime.from_string(raw_email)
                subject = eml.subject
                eml_header_from = eml.headers.get('From')
                eml_from = addresslib.address.parse(eml_header_from)
                from_address = eml_from.address
                from_display_name = eml_from.display_name
                eml_header_to = eml.headers.get('To')
                eml_header_cc=eml.headers.get('Cc')
                eml_time = eml.headers.get('Date')
                self.attachEml1(eml)
                eml_body = self.contentEml(eml)
                htmltext = self.HtmlParser(eml_body, eml_file) #解析HTML
            with open("fileDIR/Eml_Text.txt", 'w') as file:
                file.write("subject: " + subject + "\n")
                file.write("name: "+ eml_header_from + "\n")
                file.write("name: "+ eml_header_to + "\n")
                file.write("Cc: "+ str(eml_header_cc) + "\n")
                file.write("time: "+ eml_time + "\n")
                file.write("htmltext: " + htmltext + "\n")



    
if __name__ == "__main__":
    # main()
    eml_list = ['555666.eml']
    ED = EmlReader(eml_list, "dDIR/", "IMAGE/")
    ED.emlAnayalyse()


