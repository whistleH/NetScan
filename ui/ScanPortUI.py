from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QInputDialog, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt

from ui.staticValue import font_14, font_16B, font_margin

from ui.ScanHostUI import ScanInputDialog, parse_ips
from scanport import *



def parse_ports(port_str):
    valid_ports = []
    
    for part in port_str.split(','):
        part = part.strip()  # Remove any surrounding white space
        if '-' in part:  # Check if the part is a port range
            start, end = part.split('-')
            if start.isdigit() and end.isdigit() and 1 <= int(start) <= 65535 and 1 <= int(end) <= 65535 and int(start) <= int(end):
                # If both start and end are valid ports, add them to the list
                valid_ports.extend(range(int(start), int(end) + 1))
        else:  # The part is a single port
            if part.isdigit() and 1 <= int(part) <= 65535:
                # If the port is valid, add it to the list
                valid_ports.append(int(part))
    return valid_ports

class ScanPortTab(QWidget):
    def __init__(self):
        super().__init__()

        self.inner_ports = {}
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
        self.label_ip = QLabel('IP:')
        self.label_ip.setFont(font_16B)
        self.h_layout1.addWidget(self.label_ip, 1)

        self.lineEdit_ip = QLineEdit()
        self.lineEdit_ip.setFont(font_16B)
        self.h_layout1.addWidget(self.lineEdit_ip, 10)
        
        self.scan_option = QComboBox()
        # ACK / SYN / FIN / XMAS / NULL
         
        self.scan_option.setFont(font_16B)
        self.scan_option.addItem('ACK')
        self.scan_option.addItem('SYN')
        self.scan_option.addItem('FIN')
        self.scan_option.addItem('XMAS')
        self.scan_option.addItem('NULL')
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
        self.h_layout4 = QHBoxLayout() 
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["标号", "端口号", "状态", "服务名"])
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏行号
        self.h_layout4.addWidget(self.tableWidget, 4)
        
        self.right_layout = QVBoxLayout()
        
        self.button_start = QPushButton('开始扫描')
        self.button_start.setFont(font_16B)
        self.button_start.clicked.connect(self.on_button_start)
        self.right_layout.addWidget(self.button_start)
        
        
        self.button_clear = QPushButton('清空输入')
        self.button_clear.setFont(font_16B)
        self.button_clear.clicked.connect(self.on_button_clear)
        self.right_layout.addWidget(self.button_clear)
        
        self.setting_button = QPushButton('线程设置')
        self.setting_button.setFont(font_16B)
        self.setting_button.clicked.connect(self.on_setting)
        self.right_layout.addWidget(self.setting_button)
        
        self.right_layout.addStretch()
        
        self.h_layout4.addLayout(self.right_layout, 1)
        
        
        # self.button_clear = QPushButton('清空输入')
        # self.button_clear.setFont(font_16B)
        # self.button_clear.clicked.connect(self.on_button_clear)
        
        self.layout.addLayout(self.h_layout4)
        
        

    def addRow(self, data):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        
        # data = {rowPosition: (22, 'Open', 'SSH')}  # replace with your data

        for id, (port, status, service) in data.items():
            id_item = QTableWidgetItem(str(id))
            id_item.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(rowPosition, 0, id_item)

            port_item = QTableWidgetItem(str(port))
            port_item.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(rowPosition, 1, port_item)

            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(rowPosition, 2, status_item)

            if service == '':
                service = 'Unknown'
            service_item = QTableWidgetItem(service)
            service_item.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(rowPosition, 3, service_item)
            
    # 添加端口
    def on_button_add(self):
        add_win = ScanInputDialog('添加端口', '请输入端口:')
        if add_win.exec():
            port = add_win.textValue()
            # 重复添加
            if port in self.inner_ports.keys():
                QMessageBox.warning(self, "添加失败", "重复的端口号")
            else:   
                port_list = parse_ports(port)
                if len(port_list) == 0:
                    QMessageBox.warning(self, "添加失败", "错误的端口格式")
                else:
                    ss = ''
                    self.inner_ports[port] = port_list
                    for p in self.inner_ports:
                        ss += f"{p} "
                    ss.strip()
                    self.lineEdit_result.setText(ss)

    # 删除端口
    def on_button_del(self):
        del_win = ScanInputDialog('删除端口', '请输入要删除的端口:')
        if del_win.exec():
            port  = del_win.textValue();
            if port:
                current_text = self.lineEdit_result.text()
                if port in current_text.split(' '):
                    new_text = ' '.join([line for line in current_text.split(' ') if line != port])
                    self.lineEdit_result.setText(new_text)
                    if port in self.inner_ports:
                        del self.inner_ports[port]
                        
                else:
                    QMessageBox.warning(self, '删除失败', 'IP不存在')

    # 清理输出
    def on_button_clear(self):
        self.inner_ports = {}
        self.lineEdit_result.clear()
        self.lineEdit_ip.clear()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

        self.tableWidget.setHorizontalHeaderLabels(["标号", "端口号", "状态", "服务名"])
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏行号

    # 运行扫描
    def on_button_start(self):
        ip = self.lineEdit_ip.text()
        if(len(parse_ips(ip)) != 1):
            QMessageBox.critical(self, "错误", "ip地址格式错误")
        elif(len(self.inner_ports.keys()) <= 0):
            QMessageBox.critical(self, "错误", "未输入端口号")
        else:
            # 重制输出
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(["标号", "端口号", "状态", "服务名"])
            self.tableWidget.verticalHeader().setVisible(False)  # 隐藏行号
        
            port_list = [int(value) for sublist in self.inner_ports.values() for value in sublist] 
            func_type = self.scan_option.currentText()
            portscanner = PortScanner(ip, port_list, get_scan_func(func_type), thread_limit=self.thread_n)
            results = portscanner.start()
            results = dict(sorted(results.items()))
            for res in results:
                self.addRow({res: results[res]})
        
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