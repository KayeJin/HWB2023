import Reader
from openpyxl import load_workbook

class ExcelReader():
    
    def __init__(self, src: str, office_list = []) -> None:
        self.src = src
        self.office_list = office_list

    def getText(self):
        res = []
        for file in self.office_list:
            if file.split('.')[-1] == 'xlsx':
                excel = load_workbook(file)
                sheets = excel.sheetnames
                for i in range(len(sheets)): #获取workbook中所有表格
                    # sheet = excel.get_sheet_by_name(sheets[i])
                    sheet = excel[sheets[i]]
                    for m in range(sheet.min_column, sheet.max_column+1):
                        for n in range(sheet.min_row, sheet.max_row+1):
                            cell = sheet.cell(n,m).value
                            res.append(str(cell)+" ")
                        res.append("\n") 
        with open('../excel_text', 'w') as f:
            for i in res:
                f.write(i)

if __name__ == "__main__":
    R = Reader.Reader('dDIR/')
    R.file_reader()
    ER = ExcelReader(R.src, R.office_list)
    ER.getText()