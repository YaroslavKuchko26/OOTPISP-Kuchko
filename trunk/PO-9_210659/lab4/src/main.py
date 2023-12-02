import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, Qt
from PyQt5 import uic
import random


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('mainwindow.ui', self)
        self.tableView.horizontalHeader().setDefaultSectionSize(40)
        self.tableView.verticalHeader().setDefaultSectionSize(30)
        self.tableView.setSelectionMode(QTableWidget.SingleSelection)
        self.generate()

    def on_tableView_clicked(self, index):
        row, column = index.row(), index.column()
        model = self.tableView.model()
        value = model.data(index, role=Qt.DisplayRole)

        self.label_5.setText("({}, {})".format(row + 1, column + 1))
        self.label_6.setText("{}".format(row * 10 + column + 1))
        self.label_7.setText("{}".format(value * value))
        self.label_8.setText("{}".format(value * value * value))

    def generate(self):
        table = QTableWidget(10, 10)

        for i in range(10):
            for j in range(10):
                random_number = random.randint(0, 99)
                item = QTableWidgetItem(str(random_number))
                table.setItem(i, j, item)

        self.tableView.setModel(table.model())
        self.label_5.clear()
        self.label_6.clear()
        self.label_7.clear()
        self.label_8.clear()

    def on_pushButton_clicked(self):
        self.generate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

