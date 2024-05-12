from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import QtGui
from giris_ui import Ui_MainWindow
from seyahat import Uye
from ana import AnaSayfa
from kayit import KayitSayfa
from veritabani import Veritabani
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

class arayuz(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.qtprogram = Ui_MainWindow()
        self.qtprogram.setupUi(self)
        self.qtprogram.girisButon.clicked.connect(self.girisyap)
        kayitsayfa = KayitSayfa()
        self.qtprogram.kayitButon.clicked.connect(lambda: kayitsayfa.show())
        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(self.girisyap)
        self.qtprogram.girisButon.setFocusPolicy(Qt.StrongFocus)
        self.qtprogram.sifreLine.setEchoMode(QLineEdit.Password)

    def girisyap(self):
        kullaniciadi = self.qtprogram.adLine.text()
        sifre = self.qtprogram.sifreLine.text()
        Veritabani.query('SELECT * FROM kullanicilar WHERE kullaniciadi = ? AND sifre = ?', (kullaniciadi, sifre))
        sql = Veritabani.fetchone()

        if sql is None:
            QMessageBox.warning(self, "Giris", "Kullanıcı adı veya şifre yanlış.", QMessageBox.Ok)
            return

        uye = Uye(*sql)
        self.anasayfa = AnaSayfa(uye)
        self.anasayfa.show()
        self.close()


app = QApplication([])
pencere = arayuz()
pencere.show()
app.exec_()