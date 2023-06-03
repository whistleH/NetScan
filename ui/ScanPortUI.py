from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, ComboBox, QInputDialog, QPushButton, QTextEdit, QMessageBox
from ui.staticValue import font_14, font_16B, font_margin

class TemplateTab(QWidget):
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
        self.h_layout1.addWidget(self.lineEdit_ip, 10)
        
        self.label_blank = QLabel('    ', 4)
        self.label_blank.setFont(font_16B)
        self.h_layout1.addWidget(self.label_blank)
        
        self.button_clear = QPushButton('清空输入')
        self.button_clear.setFont(font_16B)
        self.h_layout1.addWidget(self.button_clear, 4)
        self.button_clear.clicked.connect(self.on_button_clear)

        self.layout.addLayout(self.h_layout1)
        
        # 边距空行
        margin_line = QHBoxLayout()
        margin_line_content = QLabel('     ')
        margin_line_content.setFont(font_margin)
        margin_line.addWidget(margin_line_content)
        self.layout.addLayout(margin_line)

        # "Result: " + 输入框 + 两个按钮
        self.h_layout2 = QHBoxLayout()
        
        self.label_result = QLabel('端口列表:')
        self.label_result.setFont(font_16B)
        self.h_layout2.addWidget(self.label_result, 1)

        self.lineEdit_result = QLineEdit()
        self.lineEdit_result.setFont(font_16B)
        self.lineEdit_result.setReadOnly(True)
        self.h_layout2.addWidget(self.lineEdit_result, 8)

        self.button_submit = QPushButton('添加')
        self.button_submit.setFont(font_16B)
        self.h_layout2.addWidget(self.button_submit, 2)
        self.button_submit.clicked.connect(self.on_button_add)

        self.button_clear = QPushButton('移除')
        self.button_clear.setFont(font_16B)
        self.h_layout2.addWidget(self.button_clear, 2)
        self.button_clear.clicked.connect(self.on_button_del)
        
        self.layout.addLayout(self.h_layout2)
        
        # 空行
        self.h_layout3 = QHBoxLayout() 
        self.label_blank_3 = QLabel('    ')
        self.label_blank_3.setFont(font_margin)
        self.h_layout3.addWidget(self.label_blank_3)
        self.layout.addLayout(self.h_layout3)
        
        
        
        # 下方表格输出
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["标号", "端口号", "状态", "服务名"])
        self.tableWidget.verticalHeader().setVisible(False)  # hide the vertical header
        


    def on_button_add(self):
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

    def on_button_del(self):
        self.lineEdit_ip.clear()
        self.checkbox1.setChecked(False)
        self.checkbox2.setChecked(False)
        self.checkbox3.setChecked(False)
        self.checkbox4.setChecked(False)
        self.lineEdit_result.clear()
        self.textEdit.clear()

    def on_button_clear():
        pass
