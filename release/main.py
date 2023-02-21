import sqlite3
import sys
from UI.addEditCoffeeForm import Ui_MainWindow as write_ui
from UI.readCoffeeForm import Ui_MainWindow as read_ui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow, write_ui, read_ui):
    def __init__(self):
        super().__init__()
        self.par = write_ui
        self.change_to_write()
        self.par = read_ui
        self.change_to_read()

    def setupUi(self, MainWindow):
        self.par.setupUi(self, self)

    def loadTable(self, table_name):
        con = sqlite3.connect(table_name)
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM coffee_data""").fetchall()
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        con.close()

    def change_to_read(self):
        self.par = read_ui
        self.setupUi(self)
        self.loadTable('data/coffee.sqlite')
        self.write_b.clicked.connect(self.change_to_write)

    def change_to_write(self):
        self.par = write_ui
        self.setupUi(self)
        self.loadTable('data/coffee.sqlite')
        self.read_b.clicked.connect(self.change_to_read)
        self.add_b.clicked.connect(self.add)
        self.save_b.clicked.connect(self.save)

    def save(self):
        data = []
        for i in range(self.tableWidget.rowCount()):
            row = []
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    row.append(item.text())
            if '' in row:
                continue
            data.append(tuple(row))
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        try:
            cur.execute("""DELETE FROM coffee_data""")
            cur.executemany(f"""INSERT INTO coffee_data VALUES (?, ?, ?, ?, ?, ?, ?)""", data)
            con.commit()
        except Exception:
            pass
        con.close()

    def add(self):
        self.tableWidget.setRowCount(
            self.tableWidget.rowCount() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
