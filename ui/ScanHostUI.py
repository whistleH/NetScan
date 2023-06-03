from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QInputDialog, QPushButton, QTextEdit, QMessageBox
from ui.staticValue import font_14, font_16B, font_margin

import re

class ScanInputDialog(QDialog):
    def __init__(self, title, desp ,parent=None):
        super(ScanInputDialog, self).__init__(parent)
        
        self.setWindowTitle(title)

        self.label = QLabel(desp)
        self.label.setFont(font_14)

        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(font_14)

        self.button = QPushButton('ok')
        self.button.setFont(font_14)
        self.button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def textValue(self):
        return self.lineEdit.text()




class ScanHostTab(QWidget):
    def __init__(self, parent=None):
        super(ScanHostTab, self).__init__(parent)

        ''' 变量部分 '''
        self.ips_inner = {}   # 存放所有ip实际数据
         
        
        ''' 组件部分 '''
        # Set layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Left part
        self.left_layout = QVBoxLayout()
        

        # 两个按钮设置
        self.button_add_ip = QPushButton('添加IP')
        self.button_add_ip.setFont(font_16B)
        self.button_add_ip.clicked.connect(self.add_ip)
        self.button_delete_ip = QPushButton('删除IP')
        self.button_delete_ip.setFont(font_16B)
        self.button_delete_ip.clicked.connect(self.delete_ip)
        # 将两个按钮添加至组件
        self.h_layout_buttons = QHBoxLayout()
        self.h_layout_buttons.addWidget(self.button_add_ip)
        self.h_layout_buttons.addWidget(self.button_delete_ip)
        self.left_layout.addLayout(self.h_layout_buttons)

        # 左侧下方文本框
        self.text_edit_ips = QTextEdit()
        self.text_edit_ips.setFont(font_14)
        self.text_edit_ips.setReadOnly(True)
        self.left_layout.addWidget(self.text_edit_ips)

        self.layout.addLayout(self.left_layout, 2)

        # Middle part
        self.middle_layout = QVBoxLayout()
        self.middle_layout.addStretch()
        
        # 中间选择扫描类型
        self.h_layout_select = QHBoxLayout()
        self.select_label = QLabel("扫描类型: ")
        self.select_label.setFont(font_14)
        self.h_layout_select.addWidget(self.select_label)   # 添加标签
        
        self.scan_option = QComboBox()
        self.scan_option.setFont(font_16B)
        self.scan_option.addItem('ICMP')
        self.scan_option.addItem('ACK')
        self.scan_option.addItem('SYN')
        self.scan_option.addItem('UDP')
        self.h_layout_select.addWidget(self.scan_option)   # 添加下拉栏
        self.middle_layout.addLayout(self.h_layout_select)  

        self.button_start_scan = QPushButton('开始扫描')
        self.button_start_scan.setFont(font_16B)
        self.button_start_scan.clicked.connect(self.start_scan)
        self.middle_layout.addWidget(self.button_start_scan)
        
        self.button_start_clear = QPushButton('清空输入')
        self.button_start_clear.setFont(font_16B)
        self.button_start_clear.clicked.connect(self.clear_ip)
        self.middle_layout.addWidget(self.button_start_clear)
        
        self.middle_layout.addStretch()
        

        self.layout.addLayout(self.middle_layout, 1)

        # Right part
        self.right_layout = QVBoxLayout()

        self.label_scan_result = QLabel('扫描结果')
        self.label_scan_result.setFont(font_16B)
        self.right_layout.addWidget(self.label_scan_result)

        self.text_edit_scan_result = QTextEdit()
        self.text_edit_scan_result.setFont(font_14)
        self.text_edit_scan_result.setReadOnly(True)
        self.right_layout.addWidget(self.text_edit_scan_result)

        self.layout.addLayout(self.right_layout, 2)

    def add_ip(self):
        add_win = ScanInputDialog('添加IP', '请输入IP:')
        if add_win.exec():
            ip = add_win.textValue()
            # 重复添加
            if ip in self.ips_inner.keys():
                QMessageBox.warning(self, "添加失败", "重复的ip地址")
            else:   
                ip_list = self.parse_ips(ip)
                if len(ip_list) == 0:
                    QMessageBox.warning(self, "添加失败", "错误的ip地址格式")
                else:
                    self.text_edit_ips.append(ip)
                    self.ips_inner[ip] = ip_list

    def delete_ip(self):
        del_win = ScanInputDialog('删除IP', '请输入要删除的IP:')
        if del_win.exec():
            ip  = del_win.textValue();
            if ip:
                current_text = self.text_edit_ips.toPlainText()
                if ip in current_text.split('\n'):
                    new_text = '\n'.join([line for line in current_text.split('\n') if line != ip])
                    self.text_edit_ips.setText(new_text)
                    if ip in self.ips_inner:
                        del self.ips_inner[ip]
                        
                else:
                    QMessageBox.warning(self, '删除失败', 'IP不存在')

    def start_scan(self):
        selected_option = self.scan_option.currentText()
        # Here you start your actual scanning operation
        # And append results to self.text_edit_scan_result
        self.text_edit_scan_result.append(f'开始 {selected_option} 扫描...')
        
    def clear_ip(self):
        self.text_edit_ips.clear()
        self.ips_inner = {}
        self.text_edit_scan_result.clear()
        pass
    
    def parse_ips(self, ip_string):
        def is_valid_ip(ip):
            parts = list(map(int, ip.split(".")))
            return len(parts) == 4 and all(0 <= part < 256 for part in parts)
        
        def generate_ips(start, end):
            start, end = int(start), int(end)
            if start > end or start < 0 or end > 255:
                return []
            return [f"192.168.1.{i}" for i in range(start, end+1)]
        
        ips = []
        matches = re.fullmatch(r"192\.168\.1\.(\d+(-\d+)?)", ip_string)
        
        if matches is not None:
            match = matches.group(1)
            if '-' in match:
                start, end = match.split('-')
                ips.extend(generate_ips(start, end))
            else:
                ip = f"192.168.1.{match}"
                if is_valid_ip(ip):
                    ips.append(ip)
                    
        return ips
