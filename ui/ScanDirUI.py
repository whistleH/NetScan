from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QInputDialog, QPushButton, QTextEdit, QMessageBox
from ui.staticValue import font_14, font_16B, font_margin

from ui.ScanHostUI import ScanInputDialog, parse_ips
from ui.ScanPortUI import parse_ports
from scandir import DirScanner
import re

class ScanDirTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        

        # "IP: " + 输入框 + 四个复选框
        margin_line = QHBoxLayout()
        margin_line_content = QLabel('     ')
        margin_line_content.setFont(font_margin)
        margin_line.addWidget(margin_line_content)
        self.layout.addLayout(margin_line)
        
        self.h_layout1 = QHBoxLayout()
        self.label_ip = QLabel('URL:')
        self.label_ip.setFont(font_16B)
        self.h_layout1.addWidget(self.label_ip, 1)

        self.lineEdit_ip = QLineEdit()
        self.lineEdit_ip.setFont(font_16B)
        self.h_layout1.addWidget(self.lineEdit_ip, 7)
        
        self.label_ip2 = QLabel("   ")
        self.label_ip2.setFont(font_16B)
        self.h_layout1.addWidget(self.label_ip2, 1)
        
        self.button_submit = QPushButton('扫描')
        self.button_submit.setFont(font_16B)
        self.h_layout1.addWidget(self.button_submit, 2)
        self.button_submit.clicked.connect(self.on_button_start)

        self.button_clear = QPushButton('清空')
        self.button_clear.setFont(font_16B)
        self.h_layout1.addWidget(self.button_clear, 2)
        self.button_clear.clicked.connect(self.on_button_clear)


        self.layout.addLayout(self.h_layout1)
        
        # 边距空行
        margin_line = QHBoxLayout()
        margin_line_content = QLabel('     ')
        margin_line_content.setFont(font_margin)
        margin_line.addWidget(margin_line_content)
        self.layout.addLayout(margin_line)

        
        # 空行
        self.h_layout3 = QHBoxLayout() 
        self.label_blank_3 = QLabel('    ')
        self.label_blank_3.setFont(font_margin)
        self.h_layout3.addWidget(self.label_blank_3)
        self.layout.addLayout(self.h_layout3)
        
        # 下方日志输出
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(font_14)
        self.textEdit.setStyleSheet("background-color: black; color: white;")
        self.layout.addWidget(self.textEdit, 5)
    
    # 清理输出
    def on_button_clear(self):
        self.lineEdit_ip.clear()
        self.textEdit.clear()

    # 运行扫描
    def on_button_start(self):
        url_str = self.lineEdit_ip.text()
        url_pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

        # 在文本中找出所有的 URL
        urls = re.findall(url_pattern, url_str)

        # 打印所有的 URL
        if len(urls) == 1:    
            dirscanner = DirScanner(urls[0], thread_limit=5)
            result = dirscanner.start()

            
            output = f"目录为: {result}"
            self.textEdit.setText(output)
        else:
            QMessageBox.critical(self, "错误", "URL格式错误")

        
            