from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from duzenle_ui import Ui_Form
from PyQt5 import QtCore
from datetime import datetime
from veritabani import Veritabani
from seyahat import *
from PyQt5.QtCore import pyqtSignal


class DuzenleSayfa(QWidget):
    kaydet_sinyal = pyqtSignal()
    def __init__(self, uye) -> None:
        super().__init__()
        self.form = Ui_Form()
        self.form.setupUi(self)
        self.uye = uye
        self.form.baslangicBox.currentIndexChanged.connect(self.varisrotalar)
        Veritabani.query("select * from sehirler")
        sehirlersql = Veritabani.fetchall()
        for id,ad in sehirlersql:
            self.form.baslangicBox.addItem(ad,id)
        self.form.varisBox.currentIndexChanged.connect(self.gorunumguncelle)
        self.form.pushButton.clicked.connect(self.kaydet)

    def goster(self):
        self.varisrotalar()
        self.show()

    def varisrotalar(self):
        self.index = 0
        baslangic = self.form.baslangicBox.currentData()
        Veritabani.query("select * from rotalar where baslangicID=?",(baslangic,))
        rotalarsql = Veritabani.fetchall()
        rotalar = []
        self.form.varisBox.clear()
        for rota in rotalarsql:
            rotaa = Rota(*rota)
            rotalar.append(rotaa)
            Veritabani.query("select * from sehirler where id=?",(rotaa.varis,))
            sehirsql = Veritabani.fetchone()
            self.form.varisBox.addItem(sehirsql[1], sehirsql[0])
        self.rotalar = rotalar

    def gorunumguncelle(self):
        if self.form.varisBox.currentIndex() < 0:
            return
        rota = self.rotalar[self.form.varisBox.currentIndex()]
        self.form.mesafeBox.setValue(rota.mesafe)
        self.form.aracBox.setValue(rota.aracsure)
        self.form.ucakBox.setValue(rota.ucaksure)
        
    def kaydet(self):
        yanit = QMessageBox.warning(self, "Rota", "İşlemi onaylıyor musunuz?", QMessageBox.Yes, QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        rota = self.rotalar[self.form.varisBox.currentIndex()]
        yenimesafe = self.form.mesafeBox.value()
        aracsure = self.form.aracBox.value()
        ucaksure = self.form.ucakBox.value()
        rota.duzenle(yenimesafe,aracsure,ucaksure)
        self.kaydet_sinyal.emit()
        QMessageBox.information(self, "Rota", "İşlem Tamamlandı", QMessageBox.Ok)
