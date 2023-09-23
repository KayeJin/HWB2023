from pyhanlp import HanLP
from pyhanlp import *
import re,os
import openpyxl

moblie_phone_pattern = re.compile(r'1[356789]\d{9}')
port_pattern = re.compile(r"^(?:[1-9]\d{0,4}|0)$")
phone_pattern = re.compile(r'0\d{2,3}-[1-9]\d{6,7}') #固话
id_pattern = re.compile(r'([1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx])|([1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2})')
email_pattern = re.compile(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)')
bank_card_pattern = re.compile(r'([1-9]{1})(\d{15}|\d{18})')
digit_pattern = re.compile(r'0|1|2|3|4|5|6|7|8|9')
Address = r'(ns|nsf|nz|nt)' #地址
ip_pattern = re.compile(r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")
r"(passwd|authorized_keys:|ssh-rsa|url:|name:|root:|BUCKET=|PATH=|OBJECTS =|buffer =|keys =|paths =|token:|ACCESSKEY=|SECRETKEY=|id_rsa|KEY=|password:|username:)：?\s*([^\\s,;]+|\"[^\"]+\")"

key_pattern = r'key|密钥|密码|口令|password|passwd|passw0rd|pw|salt|hash|auth|secure|security|authorized_keys|ssh-rsa|url|root|bucket|path|objects|buffer|token|id_rsa|user|用户名|姓名|name|host|address|地址'
user_pattern = r'user|用户名|姓名|name'
address_pattern = r'host|address|地址'
Person_Name = r'nr|nrf' #人名

za_pattern = re.compile(r"(passwd|authorized_keys:|ssh-rsa|url:|name:|root:|BUCKET=|PATH=|OBJECTS =|buffer =|keys =|paths =|token:|ACCESSKEY=|SECRETKEY=|id_rsa|KEY=|password:|username:)：?\s*([^\\s,;]+|\"[^\"]+\")")
shadow_pattern = re.compile("^(.*?):(.*?):(.*?):(.*?):(.*?):(.*?):(.*?)::$")
passwd_pattern = re.compile("^([^:]*):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*):([^:]*)$")
url_pattern = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")
patterns = [user_pattern, address_pattern, key_pattern]

def extract_student_id(text):
    # 使用HanLP进行分词和命名实体识别
    segment =HanLP.newSegment().enableNameRecognize(True)
    # p_name=NER.seg(sentence)
    # segment = HanLP.newSegment().enableNameRecognize(True)
    # term_list  = NameRecognize(text)
    term_list = segment.seg(text)
    # print(term_list)
    pattern = ['m', 'n', 'gi', 'nx']#数字、名词、计算机类、英文

    res = []
    # 遍历分词结果，查找"学号"实体
    for term in term_list:
        if term.nature.toString() in pattern:
            res.append(term.word)

    return res,term_list

def auto_check_secret(value):
    res = []
    if len(value) <= 1:
        pass # 无风险
    if re.match(id_pattern,value) and (len(value) == 15 or len(value) == 18) : #身份证 -- 高风险
        res.append("{id : " + value +"}")
    elif re.match(bank_card_pattern,value) and (len(value) == 16 or len(value) == 19): #银行卡  -- 中风险
        res.append("{bankcard : " + value +"}")
    elif re.match(phone_pattern,value): #固话 --- 中风险
        res.append("{phone : " + value +"}")
    elif re.match(email_pattern,value): #邮箱 -- 中风险
        res.append("{email : " + value +"}")
    elif re.match(moblie_phone_pattern,value) and len(value) == 11: #手机号 -- 高风险
        res.append("{mobile_phone : " + value +"}")
    elif re.match(ip_pattern, value):
        res.append("{ip : " + value +"}")
    elif re.match(url_pattern, value):
        res.append("{url : " + value +"}")
    elif re.match(passwd_pattern, value):
        res.append("{passwd : " + value +"}")
    elif re.match(shadow_pattern, value):
        res.append("{shadow : " + value +"}")
    elif re.match(za_pattern, value):
        res.append("{za : " + value +"}")
    return res

secret = '!@#$%^&*()_+}{:">?<\`~\'|"'
secret = ['\\!', '\\@', '\\#', '\\$', '\\%', '\\^', '\\&','\\*','\\(','\\)','/',',','.','<','>','?','\'','|','{','}','+','-','~','`',':',';']
def is_Chinese(text):
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def if_contain_symbol(keyword):
    symbols = "~!@#$%^&*()_+-*/<>,.[]\/"
    for symbol in symbols:
        if symbol in keyword:
            return True
    else:
        return False
ch_symbol = ['。',"，","’","‘","”","“","《","》","；"]
en_symbol = ['.', ',', '\'','\'','\"','\"','<','>',';']

def excel_file(text):
    myexcel = openpyxl.load_workbook(text)
    sheets = myexcel.sheetnames
    res = []
    for i in range(len(sheets)):
        sheet = myexcel[sheets[i]]
        dic = {}
        title = sheet.title
        for j in title:
            for pattern in patterns:
                if re.match(pattern, j):
                    dic[pattern.split('_')[0]] = j
        if dic:
            res.append(dic)
    return res

def main(text):
    text1 = text
    resres = []
    if is_Chinese(text) == False:
        if auto_check_secret(text): #直接匹配到
            resres.append(auto_check_secret(text))
        res = re.findall( key_pattern ,text, re.IGNORECASE) #key那些匹配
        for i in res: #匹配到的字段
            dic = {}
            index = text.index(i) #i的位置
            s = ''
            flag = False
            for j in text[index+len(i):]: 
                if '0'<=j<='9' or 'a'<=j<='z' or 'A'<=j<='Z' or j in ['.',',','\'',' ',';']:
                    s += j
                    flag = True
                else:
                    if flag == True:
                        break
            if s != '':
                dic[i]=s
            if dic :
                resres.append(dic)
    else:
        res, segement = extract_student_id(text)
        # print(res)
        if  res == []:
            if auto_check_secret(text):
                # print(text)
                resres.append(auto_check_secret(text))
        else:
            for i in res: #中文匹配到
                dic = {}
                if re.search( key_pattern,str(i).lower()):#密钥 ---- 该行有密钥
                    index = text.index(i) #i的位置
                    s = ''
                    flag = False
                    for j in text[index:]: 
                        if if_contain_symbol(j) or '0'<=j<='9' or 'a'<=j<='z' or 'A'<=j<='Z' or j in ['.',',','\'',' ',';'] :
                            s += j
                            flag = True
                        else:
                            if flag == True:
                                break
                    if s != '':
                        dic[i]=s
                    # dic[i]=s
                    text1.replace(s, '')
                    if dic:
                        resres.append(dic)
        
        if auto_check_secret(text1):
                resres.append(auto_check_secret(text1))
    
    return resres
  

def extract_file(fileDIR: str):
    text = []
    res = []
    for roots, dirs, files in os.walk("fileDIR/"):
        for file_path in files:
            file = os.path.join(roots, file_path)
            if file.split('.')[-1] == 'xlsx':
                res.append(excel_file(file))
            else:
                with open(file, 'r', encoding='utf-8') as f:
                    for j in f.readlines():
                        for i in range(len(ch_symbol)):
                            j.replace(ch_symbol[i],en_symbol[i])
                            res.append(main(j))

    with open("goal.txt",'w') as f:
        for line in res:
            for i in line:
                f.write(str(i) + "\n")

