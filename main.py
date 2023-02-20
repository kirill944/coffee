import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.change_to_read()

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
        uic.loadUi('main.ui', self)
        self.loadTable('coffee.sqlite')
        self.write_b.clicked.connect(self.change_to_write)

    def change_to_write(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.loadTable('coffee.sqlite')
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
            data.append(tuple(row))
        con = sqlite3.connect('coffee.sqlite')
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
