from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QTextEdit, QTabWidget, QMainWindow
from PyQt5.QtGui import QFont
import sys

from ui.ScanHostUI import ScanHostTab
from ui.ScanPortUI import ScanPortTab
from ui.ScanOsUI import ScanOsTab
from ui.ScanDirUI import ScanDirTab
# from ui.ScanHostUI import ScanTab

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('仿NMAP扫描工具')
        self.setGeometry(100, 100, 1400, 1000)
 
        self.tab_widget = QTabWidget() 
        self.setCentralWidget(self.tab_widget)

        self.tab1 = ScanHostTab()
        self.tab_widget.addTab(self.tab1, '主机扫描')

        # Other tabs ...
        self.tab2 = ScanPortTab()
        self.tab_widget.addTab(self.tab2, '端口扫描') 
        
        # self.tab3 = ScanServiceTab()
        # self.tab_widget.addTab(self.tab3, '服务扫描')
        
        self.tab4 = ScanOsTab()
        self.tab_widget.addTab(self.tab4, '系统扫描')
        
        self.tab5 = ScanDirTab()
        self.tab_widget.addTab(self.tab5, '目录扫描')


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QTabBar::tab {
            font-size: 12pt;
            width: 200px;
            height: 50px
        }
        """)
    
    win = MyWindow()
    win.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
