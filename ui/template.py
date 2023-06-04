#coding:utf-8
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QTextEdit
from PyQt5.QtGui import QFont



class TemplateTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 设置字体
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        
        # 通过字体大小设置空行边距
        margin_font = QFont()
        margin_font.setPointSize(10)
        margin_font.setBold(True)
        
        # 下方日志输出字体
        log_font = QFont()
        log_font.setPointSize(14)
        

        # "IP: " + 输入框 + 四个复选框
        margin_line = QHBoxLayout()
        margin_line_content = QLabel('     ')
        margin_line_content.setFont(margin_font)
        margin_line.addWidget(margin_line_content)
        self.layout.addLayout(margin_line)
        
        self.h_layout1 = QHBoxLayout()
        self.label_ip = QLabel('IP:')
        self.label_ip.setFont(font)
        self.h_layout1.addWidget(self.label_ip, 1)

        self.lineEdit_ip = QLineEdit()
        self.lineEdit_ip.setFont(font)
        self.h_layout1.addWidget(self.lineEdit_ip, 6)
        
        self.label_blank = QLabel('    ')
        self.label_blank.setFont(font)
        self.h_layout1.addWidget(self.label_blank)

        self.checkbox1 = QCheckBox('icmp')
        self.checkbox1.setFont(font)
        self.h_layout1.addWidget(self.checkbox1, 2)
        
        self.checkbox2 = QCheckBox('ack')
        self.checkbox2.setFont(font)
        self.h_layout1.addWidget(self.checkbox2, 2)
        
        self.checkbox3 = QCheckBox('syn')
        self.checkbox3.setFont(font)
        self.h_layout1.addWidget(self.checkbox3, 2)
        
        self.checkbox4 = QCheckBox('udp')
        self.checkbox4.setFont(font)
        self.h_layout1.addWidget(self.checkbox4, 1)

        self.layout.addLayout(self.h_layout1)
        
        # 边距空行
        margin_line = QHBoxLayout()
        margin_line_content = QLabel('     ')
        margin_line_content.setFont(margin_font)
        margin_line.addWidget(margin_line_content)
        self.layout.addLayout(margin_line)

        # "Result: " + 输入框 + 两个按钮
        self.h_layout2 = QHBoxLayout()
        
        self.label_result = QLabel('Result:')
        self.label_result.setFont(font)
        self.h_layout2.addWidget(self.label_result, 1)

        self.lineEdit_result = QLineEdit()
        self.lineEdit_result.setFont(font)
        self.lineEdit_result.setReadOnly(True)
        self.h_layout2.addWidget(self.lineEdit_result, 6)

        self.button_submit = QPushButton('提交')
        self.button_submit.setFont(font)
        self.h_layout2.addWidget(self.button_submit, 2)
        self.button_submit.clicked.connect(self.on_button_submit)

        self.button_clear = QPushButton('清空输入')
        self.button_clear.setFont(font)
        self.h_layout2.addWidget(self.button_clear, 2)
        self.button_clear.clicked.connect(self.on_button_clear)
        
        self.layout.addLayout(self.h_layout2)
        
        # 空行
        self.h_layout3 = QHBoxLayout() 
        self.label_blank_3 = QLabel('    ')
        self.label_blank_3.setFont(font)
        self.h_layout3.addWidget(self.label_blank_3)
        self.layout.addLayout(self.h_layout3)
        
        # LOG标签
        self.h_layout4 = QHBoxLayout()
        self.label_log = QLabel('日志: ')
        self.label_log.setFont(font)
        self.h_layout4.addWidget(self.label_log)
        self.layout.addLayout(self.h_layout4) 
        
        
        
        # 下方日志输出
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(log_font)
        self.textEdit.setStyleSheet("background-color: black; color: white;")
        self.layout.addWidget(self.textEdit, 5)


    def on_button_submit(self):
        # 获取参数
        ip = self.lineEdit_ip.text()
        checkbox_status1 = self.checkbox1.isChecked()
        checkbox_status2 = self.checkbox2.isChecked()
        checkbox_status3 = self.checkbox3.isChecked()
        checkbox_status4 = self.checkbox4.isChecked()

        # 根据需要处理参数
        output = f'IP: {ip}, Checkbox Status: {checkbox_status1}, {checkbox_status2}, {checkbox_status3}, {checkbox_status4}'
        
        # 将输出显示在文本框中
        self.textEdit.setText(output)

    def on_button_clear(self):
        self.lineEdit_ip.clear()
        self.checkbox1.setChecked(False)
        self.checkbox2.setChecked(False)
        self.checkbox3.setChecked(False)
        self.checkbox4.setChecked(False)
        self.lineEdit_result.clear()
        self.textEdit.clear()


