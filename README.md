# HWB2023 华为杯”第二届中国研究生网络安全创新大赛揭榜挑战赛赛题
题目一：富文本敏感信息泄露检测 
https://cpipc.acge.org.cn//cw/detail/2c90800c8093eef401809d33b36f0652/2c90801787f062ab018871a92ff078ba


依赖：
1. tesseract 5.0 
    sudo add-apt-repository -y ppa:alex-p/tesseract-ocr5
    sudo apt install -y tesseract-ocr
    sudo apt-get install tesseract-ocr-chi-sim #安装中文库
2. python-pil:  sudo apt-get install python-pil
3. pytesseract
4. libreoffice: 
    sudo apt-add-repository ppa:libreoffice/libreoffice-7-0
    sudo apt install libreoffice
    export LD_LIBRARY_PATH="/usr/lib/libreoffice/program:$LD_LIBRARY_PATH"
5. rar、unrar: 
    sudo apt-get install rar
    sudo apt-get install unrar  
6. pip install -r requirements.txt
7. paddleocr:
    pip install paddlepaddle
    pip install paddleocr


使用：
python setup.py 压缩包
即可自动化提取、分析

内容提取保存在fileDIR/文件夹中
敏感信息保存在 goal.txt文件中
