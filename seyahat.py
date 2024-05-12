from veritabani import Veritabani

class Rota:
    def __init__(self,id, baslangic, varis, mesafe, aracsure, ucaksure):
        self.id = id
        self.baslangic = baslangic
        self.varis = varis
        self.mesafe = mesafe
        self.aracsure = aracsure
        self.ucaksure = ucaksure

    def duzenle(self, yenimesafe, yeniaracsure, yeniucaksure):
        Veritabani.query("update rotalar set mesafe=?, aracsure=?, ucaksure=? where id=?",(yenimesafe, yeniaracsure, yeniucaksure, self.id))

    def kaydet(self,uye, otel):
        Veritabani.query("insert into liste (kullaniciid,rotaid,otelid) values(?,?,?)",(uye.id, self.id, otel.id))

    def sil(self,uye, otel):
        Veritabani.query("delete from liste where rotaid=? and otelid=? and kullaniciid=?",(self.id, otel.id, uye.id))

class Uye:
    def __init__(self, id, kullaniciadi, sifre, ad, soyad, telefon):
        self.id = id
        self.kullaniciadi = kullaniciadi
        self.sifre = sifre
        self.ad = ad
        self.soyad = soyad
        self.telefon = telefon

    @staticmethod
    def kayitol(kullaniciadi, sifre, ad, soyad, telefon):
        Veritabani.query('INSERT INTO kullanicilar (kullaniciadi, sifre, ad, soyad, telefon) VALUES(?, ?, ?, ?, ?)', (kullaniciadi, sifre, ad, soyad, telefon))

class Otel:
    def __init__(self,id, ad, puan, alan, fiyat, il, fotograf):
        self.id = id
        self.ad = ad
        self.puan = puan
        self.alan = alan
        self.fiyat = fiyat
        self.il = il
        self.fotograf = fotograf

        