from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ana_ui import Ui_MainWindow
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtGui
from veritabani import Veritabani
from seyahat import *
from liste import SeyahatListeSayfa
from duzenle import DuzenleSayfa

class AnaSayfa(QMainWindow):
    def __init__(self, uye) -> None:
        super().__init__()
        self.anasayfa = Ui_MainWindow()
        self.anasayfa.setupUi(self)
        self.index = 0
        self.anasayfa.sonrakiButon.clicked.connect(self.sonraki)
        self.anasayfa.oncekiButon.clicked.connect(self.onceki)
        Veritabani.query("select * from sehirler")
        sehirlersql = Veritabani.fetchall()
        self.anasayfa.baslangicBox.currentIndexChanged.connect(self.varisrotalar)
        self.uye = uye
        for id,ad in sehirlersql:
            self.anasayfa.baslangicBox.addItem(ad,id)
        self.anasayfa.varisBox.currentIndexChanged.connect(self.otelliste)
        self.otelliste()
        self.anasayfa.kaydetButon.clicked.connect(self.rotakaydet)
        listesayfa = SeyahatListeSayfa(uye)
        self.anasayfa.actionListe.triggered.connect(lambda: listesayfa.goster())
        duzenlesayfa = DuzenleSayfa(uye)
        self.anasayfa.actionRota_D_zenle.triggered.connect(lambda: duzenlesayfa.goster())
        duzenlesayfa.kaydet_sinyal.connect(self.guncelle)


    def sonraki(self):
        self.index += 1
        if len(self.oteller) == self.index:
            self.index = 0
        self.otelguncelle()

    def onceki(self):
        self.index -= 1
        if self.index == -1:
            self.index = len(self.oteller)-1
        self.otelguncelle()

    def rotagoster(self, yeni_indeks):
        self.index = yeni_indeks
        self.otelguncelle()

    def otelguncelle(self, index=None):
        if not self.oteller or self.index >= len(self.oteller):
            return
        
        otel = self.oteller[self.index]

        self.anasayfa.foto.setPixmap(QtGui.QPixmap("fotograflar/" + otel.fotograf))
        self.anasayfa.otelisimLabel.setText(otel.ad)
        self.anasayfa.odaLabel.setText(f'{otel.alan} m²')
        self.anasayfa.fiyatLabel.setText(f'{otel.fiyat} TL')
        puan = ""
        for i in range(1,otel.puan+1):
            puan += "★"
        self.anasayfa.puanLabel.setText(puan)
        rota = self.rotalar[self.anasayfa.varisBox.currentIndex()]
        Veritabani.query("select * from liste where rotaid=? and otelid=?", (rota.id, otel.id))
        kayit = Veritabani.fetchone()
        if kayit is None:
            self.anasayfa.kaydetButon.setText("Kaydet")
        else:
            self.anasayfa.kaydetButon.setText("Sil")

    def varisrotalar(self, index=None):
        if index is None:
            self.index = 0
        baslangic = self.anasayfa.baslangicBox.currentData()
        Veritabani.query("select * from rotalar where baslangicID=?",(baslangic,))
        rotalarsql = Veritabani.fetchall()
        rotalar = []
        self.anasayfa.varisBox.clear()
        for rota in rotalarsql:
            rotaa = Rota(*rota)
            rotalar.append(rotaa)
            Veritabani.query("select * from sehirler where id=?",(rotaa.varis,))
            sehirsql = Veritabani.fetchone()
            self.anasayfa.varisBox.addItem(sehirsql[1], sehirsql[0])
        self.rotalar = rotalar
        
    def otelliste(self, index=None):
        if index is None:
            self.index = 0
        if self.anasayfa.varisBox.currentIndex() < 0:
            return
        sehir = self.anasayfa.varisBox.currentText()
        Veritabani.query("select * from oteller where il=?",(sehir,))
        otellersql = Veritabani.fetchall()
        oteller = []
        for otel in otellersql:
            oteller.append(Otel(*otel))
        self.oteller = oteller  # oteller listesini self.oteller özelliğine atama
        self.index = 0
        self.otelguncelle()
        rota = self.rotalar[self.anasayfa.varisBox.currentIndex()]
        self.anasayfa.mesafeLabel.setText(f"{rota.mesafe} KM")
        self.anasayfa.aracLabel.setText(f"{rota.aracsure} Saat")
        self.anasayfa.ucakLabel.setText(f"{rota.ucaksure} Saat")
        
    def rotakaydet(self):
        rota = self.rotalar[self.anasayfa.varisBox.currentIndex()]
        yanit = QMessageBox.warning(self, "Rota", "İşlemi onaylıyor musunuz?", QMessageBox.Yes, QMessageBox.No)
        if yanit == QMessageBox.No:
            return
        butonyazi = self.anasayfa.kaydetButon.text()
        otel = self.oteller[self.index]
        if butonyazi == "Kaydet":
            rota.kaydet(self.uye, otel)
            self.anasayfa.kaydetButon.setText("Sil")
        else:
            rota.sil(self.uye, otel)
            self.anasayfa.kaydetButon.setText("Kaydet")
        QMessageBox.information(self,"Rota", "İşlem Tamamlandı", QMessageBox.Ok)

    def guncelle(self):
        self.varisrotalar(0)
        self.otelliste(0)