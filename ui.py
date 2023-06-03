from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QTextEdit, QTabWidget, QMainWindow
from PyQt5.QtGui import QFont
import sys

from ui.ScanHostUI import ScanHostTab
from ui.template import TemplateTab
# from ui.ScanHostUI import ScanTab

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('My First PyQt5 App')
        self.setGeometry(100, 100, 1400, 1000)

        self.tab_widget = QTabWidget() 
        self.setCentralWidget(self.tab_widget)

        self.tab1 = ScanHostTab()
        self.tab_widget.addTab(self.tab1, '主机扫描')

        # Other tabs ...
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, 'Tab2')
        
        self.tab3 = QWidget()
        self.tab_widget.addTab(self.tab3, 'Tab3')
        
        self.tab4 = QWidget()
        self.tab_widget.addTab(self.tab4, 'Tab4')
        
        self.tab5 = TemplateTab()
        self.tab_widget.addTab(self.tab5, 'Tab5')


def main():
    app = QApplication(sys.argv)
    
    win = MyWindow()
    win.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
