import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont, QColor

class TableUI(QMainWindow):
    def __init__(self):
        super(TableUI, self).__init__()
        self.setWindowTitle("Kayıt Verileri")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(10, 10, 780, 580)

        self.show_data()

    def show_data(self):
        data = self.get_data_from_database()

        if not data:
            self.show_message("Veritabanında veri bulunamadı.")
            return

        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data[0]))

        for row_number, row_data in enumerate(data):
            for column_number, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                self.table_widget.setItem(row_number, column_number, item)

        # Yazıları tam sütün içine sığdırmak için boyut ayarlaması yapalım
        self.table_widget.resizeColumnsToContents()

        # Arka plan rengini beyaz yapalım
        self.setStyleSheet("background-color: white;")

        # Yazı tipini italik yapalım
        font = QFont()
        font.setItalic(True)
        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):
                self.table_widget.item(row, column).setFont(font)

    def get_data_from_database(self):
        try:
            baglanti = sqlite3.connect("kayit.db")
            imlec = baglanti.cursor()

            # Tablo var mı diye kontrol et
            imlec.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Kayit';")
            tablo_var_mi = imlec.fetchall()

            if not tablo_var_mi:
                return []

            # Veritabanından verileri çek
            imlec.execute("SELECT * FROM Kayit")
            data = imlec.fetchall()

            baglanti.close()

            return data
        except sqlite3.Error as e:
            print("Veritabanı hatası:", e)
            return []

    def show_message(self, message):
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(1)
        item = QTableWidgetItem(message)
        self.table_widget.setItem(0, 0, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    table_ui = TableUI()
    table_ui.show()

    sys.exit(app.exec_())
