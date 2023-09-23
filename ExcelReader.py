import Reader
from openpyxl import load_workbook
import shutil
class ExcelReader():
    
    def __init__(self, src: str, office_list: []) -> None:
        self.src = src
        self.office_list = office_list

    def getText(self):
        for file in self.office_list:
            if file.split('.')[-1] == 'xlsx':
                shutil.copyfile( file, "fileDIR/"+file.split('/')[-1])

if __name__ == "__main__":
    R = Reader.Reader('dDIR/')
    R.file_reader()
    ER = ExcelReader(R.src, R.office_list)
    ER.getText()