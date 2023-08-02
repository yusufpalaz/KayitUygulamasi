import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem
import sqlite3

class KayitForm(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kayıt Uygulaması")

        self.label_ad = QLabel("Ad:")
        self.input_ad = QLineEdit()

        self.label_soyad = QLabel("Soyad:")
        self.input_soyad = QLineEdit()

        self.label_sirket = QLabel("Şirket:")
        self.input_sirket = QLineEdit()

        self.label_seviye = QLabel("Bilgisayar Derseni Seviyorum:")
        self.combo_seviye = QComboBox()
        self.combo_seviye.addItems(["Evet", "Hayır"])

        self.label_kullanım = QLabel("Bilgisayarı Ne İçin Kullanıyorum:")
        self.combo_kullanım = QComboBox()
        self.combo_kullanım.addItems(["Ders çalışmak için", "Kullanmıyorum", "Filim izlemek için", "Oyun oynamak için"])

        self.button_ekle = QPushButton("Ekle")
        self.button_ekle.clicked.connect(self.ekle_kayit)

        self.button_sil = QPushButton("Sil")
        self.button_sil.clicked.connect(self.sil_kayit)

        self.button_filtre = QPushButton("Filtre")
        self.button_filtre.clicked.connect(self.filtre_kayit)

        self.table_kayitlar = QTableWidget()
        self.table_kayitlar.setColumnCount(5)
        self.table_kayitlar.setHorizontalHeaderLabels(["Ad", "Soyad", "Şirket", "Seviye", "Kullanım"])

        layout = QVBoxLayout()
        layout.addWidget(self.label_ad)
        layout.addWidget(self.input_ad)
        layout.addWidget(self.label_soyad)
        layout.addWidget(self.input_soyad)
        layout.addWidget(self.label_sirket)
        layout.addWidget(self.input_sirket)
        layout.addWidget(self.label_seviye)
        layout.addWidget(self.combo_seviye)
        layout.addWidget(self.label_kullanım)
        layout.addWidget(self.combo_kullanım)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_ekle)
        button_layout.addWidget(self.button_sil)
        button_layout.addWidget(self.button_filtre)

        layout.addLayout(button_layout)
        layout.addWidget(self.table_kayitlar)

        self.setLayout(layout)

        self.baglanti_kur()
        self.verileri_goster()

    def baglanti_kur(self):
        self.baglanti = sqlite3.connect("kayit.db")
        self.islem = self.baglanti.cursor()

        self.islem.execute("CREATE TABLE IF NOT EXISTS Kayit (Ad TEXT, Soyad TEXT, Sirket TEXT, Seviye TEXT, Kullanım TEXT)")
        self.baglanti.commit()

    def ekle_kayit(self):
        ad = self.input_ad.text()
        soyad = self.input_soyad.text()
        sirket = self.input_sirket.text()
        seviye = self.combo_seviye.currentText()
        kullanım = self.combo_kullanım.currentText()

        self.islem.execute("INSERT INTO Kayit (Ad, Soyad, Sirket, Seviye, Kullanım) VALUES (?, ?, ?, ?, ?)", (ad, soyad, sirket, seviye, kullanım))
        self.baglanti.commit()

        self.input_ad.clear()
        self.input_soyad.clear()
        self.input_sirket.clear()

        self.verileri_goster()

    def sil_kayit(self):
        # Silme işlevselliği buraya eklenmeli
        pass

    def filtre_kayit(self):
        # Filtreleme işlevselliği buraya eklenmeli
        pass

    def verileri_goster(self):
        self.islem.execute("SELECT * FROM Kayit")
        kayitlar = self.islem.fetchall()

        self.table_kayitlar.setRowCount(0)

        for row_number, kayit in enumerate(kayitlar):
            self.table_kayitlar.insertRow(row_number)
            for column_number, deger in enumerate(kayit):
                self.table_kayitlar.setItem(row_number, column_number, QTableWidgetItem(str(deger)))

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = KayitForm()
    pencere.show()
    sys.exit(uygulama.exec_())
