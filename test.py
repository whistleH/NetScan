import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class AppDemo(QWidget): 
    def __init__(self):
        super().__init__()
        self.resize(400, 300)

        mainLayout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["标号", "端口号", "状态", "服务名"])
        self.tableWidget.verticalHeader().setVisible(False)  # hide the vertical header

        mainLayout.addWidget(self.tableWidget)

        self.addButton = QPushButton('Add Row')
        self.addButton.clicked.connect(self.addRow)
        mainLayout.addWidget(self.addButton)

        self.setLayout(mainLayout)

    def addRow(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        
        data = {rowPosition: (22, 'Open', 'SSH')}  # replace with your data

        for id, (port, status, service) in data.items():
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(id)))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(port)))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(status))
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(service))

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
