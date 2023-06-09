from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QInputDialog, QPushButton, QTextEdit, QMessageBox
from ui.staticValue import font_14, font_16B, font_margin

from ui.ScanHostUI import ScanInputDialog, parse_ips
from ui.ScanPortUI import parse_ports
from scandir import DirScanner
import re


def filter_status(status, keyword, str_list):
    # 首先验证输入的状态码
    if len(status) != 3 or not status[0].isdigit() or int(status[0]) not in [2, 3, 4, 5] or (status[1:] != "xx" and not status[1:].isdigit()):
        return 'Invalid status code'

    result = []
    for string in str_list:
        tmp_split = string.split(',')
        str_status = tmp_split[0]
        url = ''.join(tmp_split[1:])
        # str_status, url = string.split(',')
        # 检查状态码是否匹配
        if status[1:] == 'xx':
            if str_status[0] != status[0]:
                continue
        else:
            if str_status != status:
                continue
        # 检查URL是否包含关键词
        if keyword not in url:
            continue
        # 如果状态码和关键词都匹配，则将此字符串添加到结果列表中
        result.append(string)

    return result

class ScanDirTab(QWidget):
    def __init__(self):
        super().__init__()

        self.res_data = []
        self.thread_n = 1
        
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
        
        # Filter
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
        
        # 边距
        # self.marginLabel = QLabel("   ")
        # self.marginLabel.setFont(font_margin)
        # self.layout.addWidget(self.marginLabel)
        
        self.h_layout_setting = QHBoxLayout()
        self.h_layout_setting.addStretch()
        self.setting_button = QPushButton('线程设置')
        self.setting_button.setFont(font_16B)
        self.setting_button.clicked.connect(self.on_setting)
        self.h_layout_setting.addWidget(self.setting_button)
        self.layout.addLayout(self.h_layout_setting)
        
        # 过滤器
        self.filter_label = QLabel("Filter: ")
        self.filter_label.setFont(font_16B)
        self.layout.addWidget(self.filter_label)
        
        # 过滤器选项
        self.filter_setting_line = QHBoxLayout()
        # 状态码 -- 标签
        self.filter_status_lable = QLabel("状态码:")
        self.filter_status_lable.setFont(font_14)
        # 状态码 -- 输入
        self.filter_status_input = QLineEdit()
        self.filter_status_input.setFont(font_14)
        # 添加状态码过滤组件
        self.filter_setting_line.addWidget(self.filter_status_lable)
        self.filter_setting_line.addWidget(self.filter_status_input)
        
        self.filter_setting_line.addStretch()
        
        # 关键字 -- 标签
        self.filter_key_lable = QLabel("关键字:")
        self.filter_key_lable.setFont(font_14)
        # 关键字 -- 输入
        self.filter_key_input = QLineEdit()
        self.filter_key_input.setFont(font_14)
        # 添加关键字过滤器
        self.filter_setting_line.addWidget(self.filter_key_lable)
        self.filter_setting_line.addWidget(self.filter_key_input)
        
        
        self.filter_setting_line.addStretch()
        
        
        # 操作按钮添加
        self.filter_setting_button = QPushButton("过滤显示")
        self.filter_setting_button.setFont(font_14)
        self.filter_setting_button.clicked.connect(self.on_button_show)
        self.filter_setting_line.addWidget(self.filter_setting_button)
        
        # 添加过滤行
        self.layout.addLayout(self.filter_setting_line)
        
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
        self.filter_key_input.clear()
        self.filter_status_input.clear()
        self.res_data.clear()
        

    # 运行扫描
    def on_button_start(self):
        url_str = self.lineEdit_ip.text()
        url_pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

        # 在文本中找出所有的 URL
        urls = re.findall(url_pattern, url_str)

        # 打印所有的 URL
        if len(urls) == 1:    
            dirscanner = DirScanner(urls[0], thread_limit=self.thread_n)
            result = dirscanner.start()

            # log_path = 'log/aHR0cDovLzEyNy4wLjAuMTo4MC0yMDIzLTA2LTA0IDE2OjQ5OjU0LjQ3ODY0Nw=='
            log_path = result
            with open(log_path, 'r') as file:
                self.res_data = file.readlines()
                
            self.textEdit.append(f"扫描完毕, 共{len(self.res_data)}条结果, 请设置Filter显示具体结果")
            for res in self.res_data:
                self.textEdit.append(res.strip())
            # output = f"目录为: {result}"
        else:
            QMessageBox.critical(self, "错误", "URL格式错误")

    def on_button_show(self):
        filter_res = []
        if(len(self.res_data)==0):
            QMessageBox.warning(self, "", "没有可供过滤的结果")
            return
        
        status = self.filter_status_input.text()
        key_word = self.filter_key_input.text()
        if status == "" and key_word == "":
            QMessageBox.warning(self, "", "未选择过滤条件")
            
        # 先过滤状态码
        if status != "":
            filter_res = filter_status(status, key_word, self.res_data)
            if(filter_res == "Invalid status code"):
                QMessageBox.critical(self, "状态码", "状态码格式错误")
                return
            
        # 只设置关键字
        else:
            for res in self.res_data:
                if key_word in res:
                    filter_res.append(res)
        
            
        if(len(filter_res)):
            self.textEdit.setText(''.join(filter_res))
        else:
            self.textEdit.setText("None")
            
    def on_setting(self):
        set_win = ScanInputDialog('设置线程', f'请输入线程数(默认为1, 当前线程为{self.thread_n}):')
        if set_win.exec():
            thread_num = set_win.textValue()
            try:
                thread_num = int(thread_num)
            except:
                QMessageBox.warning(self, '错误', "输入非法")
                return
            
            if thread_num <= 0:
                QMessageBox.warning(self, '错误',"输入范围错误")
                return
            self.thread_n = thread_num