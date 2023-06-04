from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QInputDialog, QPushButton, QTextEdit, QMessageBox
from ui.staticValue import font_14, font_16B, font_margin

from ui.ScanHostUI import ScanInputDialog, parse_ips
from ui.ScanPortUI import parse_ports
from scanos import icmp_para_scan, tcp_para_scan


class ScanOsTab(QWidget):
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
        self.h_layout1.addWidget(self.lineEdit_ip, 9)
        
        self.label_ip2 = QLabel("   ")
        self.label_ip2.setFont(font_16B)
        self.h_layout1.addWidget(self.label_ip2, 2)
        
        self.scan_option = QComboBox()   
        self.scan_option.setFont(font_16B)
        self.scan_option.addItem('TCP')
        self.scan_option.addItem('ICMP')
        self.scan_option.currentIndexChanged.connect(self.on_update_option)
        self.h_layout1.addWidget(self.scan_option, 4)

        self.layout.addLayout(self.h_layout1)
        
        # 边距空行
        margin_line = QHBoxLayout()
        margin_line_content = QLabel('     ')
        margin_line_content.setFont(font_margin)
        margin_line.addWidget(margin_line_content)
        self.layout.addLayout(margin_line)

        # "Result: " + 输入框 + 两个按钮
        self.h_layout2 = QHBoxLayout()
        self.label_port = QLabel('端口:')
        self.label_port.setFont(font_16B)
        self.h_layout2.addWidget(self.label_port, 1)

        self.lineEdit_port = QLineEdit()
        self.lineEdit_port.setFont(font_16B)
        self.h_layout2.addWidget(self.lineEdit_port, 7)

        self.button_submit = QPushButton('扫描')
        self.button_submit.setFont(font_16B)
        self.h_layout2.addWidget(self.button_submit, 2)
        self.button_submit.clicked.connect(self.on_button_start)

        self.button_clear = QPushButton('清空')
        self.button_clear.setFont(font_16B)
        self.h_layout2.addWidget(self.button_clear, 2)
        self.button_clear.clicked.connect(self.on_button_clear)
        
        self.layout.addLayout(self.h_layout2)
        
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
        self.lineEdit_port.clear()
        self.lineEdit_ip.clear()
        self.textEdit.clear()

    # 运行扫描
    def on_button_start(self):
        ip = self.lineEdit_ip.text()
        port = self.lineEdit_port.text()
        if(len(parse_ips(ip)) != 1):
            QMessageBox.critical(self, "错误", "ip地址格式错误")
        elif (self.scan_option.currentText() == "TCP" and len(parse_ports(port)) != 1):
            QMessageBox.critical(self, "错误", "未输入端口号或者端口错误")
        else:
            # 重制输出
            if self.scan_option.currentText() == "TCP":
                resp = tcp_para_scan(ip, int(port))
            else:
                resp = icmp_para_scan(ip)
            
            output = f"协议为: {resp.keys()}\n 返回内容为: {resp.values()}"
            self.textEdit.setText(output)
            
     
    def on_update_option(self):
        if self.scan_option.currentText() == "TCP":
            self.lineEdit_port.setEnabled(True)
        else:
            self.lineEdit_port.setEnabled(False)
        
        
            