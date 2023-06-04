from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox

from ui.staticValue import font_16B, font_14, font_margin
from ui.ScanHostUI import parse_ips
from ui.ScanPortUI import parse_ports


from scanservice import get_banner

class ScanServiceTab(QWidget):
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
        self.label_ip = QLabel('IP:')
        self.label_ip.setFont(font_16B)
        self.h_layout1.addWidget(self.label_ip, 1)

        self.lineEdit_ip = QLineEdit()
        self.lineEdit_ip.setFont(font_16B)
        self.h_layout1.addWidget(self.lineEdit_ip, 8)
        
        self.label_blank = QLabel('    ')
        self.label_blank.setFont(font_16B)
        self.h_layout1.addWidget(self.label_blank, 4)

        self.layout.addLayout(self.h_layout1)
        
        # 边距空行
        margin_line = QHBoxLayout()
        margin_line_content = QLabel('     ')
        margin_line_content.setFont(font_margin)
        margin_line.addWidget(margin_line_content)
        self.layout.addLayout(margin_line)

        # 输入端口
        self.h_layout2 = QHBoxLayout()
        self.label_port = QLabel('端口:')
        self.label_port.setFont(font_16B)
        self.h_layout2.addWidget(self.label_port, 1)

        self.lineEdit_port = QLineEdit()
        self.lineEdit_port.setFont(font_16B)
        self.h_layout2.addWidget(self.lineEdit_port, 8)

        self.button_submit = QPushButton('提交')
        self.button_submit.setFont(font_16B)
        self.h_layout2.addWidget(self.button_submit, 2)
        self.button_submit.clicked.connect(self.on_button_submit)

        self.button_clear = QPushButton('清空输入')
        self.button_clear.setFont(font_16B)
        self.h_layout2.addWidget(self.button_clear, 2)
        self.button_clear.clicked.connect(self.on_button_clear)
    
        self.layout.addLayout(self.h_layout2)
        
        # 空行
        self.h_layout3 = QHBoxLayout() 
        self.label_blank_3 = QLabel('    ')
        self.label_blank_3.setFont(font_16B)
        self.h_layout3.addWidget(self.label_blank_3)
        self.layout.addLayout(self.h_layout3)
        
        # 输出标签
        self.h_layout4 = QHBoxLayout()
        self.label_out = QLabel('输出: ')
        self.label_out.setFont(font_16B)
        self.h_layout4.addWidget(self.label_out)
        self.layout.addLayout(self.h_layout4) 
        
        
        
        # 下方日志输出
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(font_14)
        self.textEdit.setStyleSheet("background-color: black; color: white;")
        self.layout.addWidget(self.textEdit, 5)


    def on_button_submit(self):
        # 获取参数
        ip = self.lineEdit_ip.text()
        port = self.lineEdit_port.text()
        if len(parse_ips(ip)) != 1:
            QMessageBox.critical(self, "错误", "ip地址格式错误")
        elif len(parse_ports(port)) != 1:
            QMessageBox.critical(self, "错误", "端口号错误") 
        else:
            self.textEdit.clear()
            output = get_banner(ip, port)
            self.textEdit.setText(output)
        # 根据需要处理参数
        
        # 将输出显示在文本框中
        

    def on_button_clear(self):
        self.lineEdit_ip.clear()
        self.lineEdit_port.clear()
        self.textEdit.clear()


