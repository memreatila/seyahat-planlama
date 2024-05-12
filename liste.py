from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from liste_ui import Ui_Form
from PyQt5 import QtCore
from datetime import datetime
from veritabani import Veritabani
from seyahat import *

class SeyahatListeSayfa(QWidget):
    def __init__(self, uye) -> None:
        super().__init__()
        self.form = Ui_Form()
        self.form.setupUi(self)
        self.uye = uye

    def goster(self):
        tablo = self.form.tablo
        tablo.setRowCount(0)
        Veritabani.query('SELECT rotaid, otelid FROM liste WHERE kullaniciid = ?', (self.uye.id,))
        kayitlarssql = Veritabani.fetchall()

        self.show()
        if kayitlarssql is None:
            return
        
        tablo.setRowCount(len(kayitlarssql))
        satir = 0
        tablo.setColumnWidth(0, 100)
        tablo.setColumnWidth(1, 100)
        tablo.setColumnWidth(2, 80)
        tablo.setColumnWidth(3, 80)
        tablo.setColumnWidth(4, 80)
        tablo.setColumnWidth(5, 100)
        tablo.setColumnWidth(6, 80)
        tablo.setColumnWidth(7, 80)


        for rotaid, otelid in kayitlarssql:
            Veritabani.query("SELECT * FROM oteller WHERE id = ?", (otelid,))
            otelsql = Veritabani.fetchone()
            otel = Otel(*otelsql)

            Veritabani.query("SELECT * FROM rotalar WHERE id = ?", (rotaid,))
            rotasql = Veritabani.fetchone()
            rota = Rota(*rotasql)

            Veritabani.query("SELECT ad FROM sehirler WHERE id = ?", (rota.varis,))
            varissql = Veritabani.fetchone()

            Veritabani.query("SELECT ad FROM sehirler WHERE id = ?", (rota.baslangic,))
            baslangicsql = Veritabani.fetchone()

            baslangiccell = QTableWidgetItem(baslangicsql[0])
            variscell = QTableWidgetItem(varissql[0])
            mesafecell = QTableWidgetItem(f"{rota.mesafe} KM")
            araccell = QTableWidgetItem(f"{rota.aracsure} Saat")
            ucakcell = QTableWidgetItem(f"{rota.ucaksure} Saat")
            puan = ""
            for i in range(1,otel.puan+1):
                puan += "★"
            otelcell = QTableWidgetItem(otel.ad)
            puancell = QTableWidgetItem(puan)
            fiyatcell = QTableWidgetItem(f"{otel.fiyat} TL")



            #Hepsinin yazısını ortala
            baslangiccell.setTextAlignment(QtCore.Qt.AlignCenter)
            variscell.setTextAlignment(QtCore.Qt.AlignCenter)
            mesafecell.setTextAlignment(QtCore.Qt.AlignCenter)
            araccell.setTextAlignment(QtCore.Qt.AlignCenter)
            ucakcell.setTextAlignment(QtCore.Qt.AlignCenter)
            puancell.setTextAlignment(QtCore.Qt.AlignCenter)
            otelcell.setTextAlignment(QtCore.Qt.AlignCenter)
            fiyatcell.setTextAlignment(QtCore.Qt.AlignCenter)


            tablo.setItem(satir, 0, baslangiccell)
            tablo.setItem(satir, 1, variscell)
            tablo.setItem(satir, 2, mesafecell)
            tablo.setItem(satir, 3, araccell)
            tablo.setItem(satir, 4, ucakcell)
            tablo.setItem(satir, 5, otelcell)
            tablo.setItem(satir, 6, puancell)
            tablo.setItem(satir, 7, fiyatcell)

            satir+=1

        #tablo.resizeColumnsToContents()