import sqlite3

class veritabani:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rotalar'")
        tablo_var_mi = self.cursor.fetchone()

        if not tablo_var_mi:  # Tablo yok
            self.cursor.execute('CREATE TABLE IF NOT EXISTS rotalar (ID INTEGER PRIMARY KEY AUTOINCREMENT, baslangicID INTEGER, varisID INTEGER, mesafe INTEGER, aracsure INTEGER, ucaksure INTEGER)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS kullanicilar (ID INTEGER PRIMARY KEY AUTOINCREMENT, kullaniciadi TEXT, sifre TEXT, ad TEXT, soyad TEXT, telefon TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS oteller (ID INTEGER PRIMARY KEY AUTOINCREMENT,ad TEXT, puan INTEGER, alan INTEGER, fiyat INTEGER, il TEXT, fotograf TEXT)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS liste (ID INTEGER PRIMARY KEY AUTOINCREMENT,kullaniciID INTEGER, rotaID INTEGER, otelID INTEGER)')
            self.cursor.execute('CREATE TABLE IF NOT EXISTS sehirler (ID INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT)')

            oteller = [
                ("Hilton", 4, 500, 300, "İstanbul", "1.jpg"),
                ("Sheraton", 5, 600, 350, "Ankara", "2.jpg"),
                ("Marriott", 4, 450, 280, "İzmir", "3.jpg"),
                ("Radisson Blu", 4, 400, 270, "Antalya", "4.jpg"),
                ("Rixos", 5, 550, 400, "Bodrum", "5.jpg"),
                ("Mövenpick", 4, 480, 320, "İstanbul", "6.jpg"),
                ("DoubleTree", 4, 420, 250, "Ankara", "7.jpg")
            ]

                        # Şehir verileri
            sehirler = [
                ("İstanbul",),
                ("Ankara",),
                ("İzmir",),
                ("Antalya",),
                ("Bodrum",)
                ]
            
            # Şehirleri ekleyelim
            self.cursor.executemany('INSERT INTO sehirler (ad) VALUES (?)', sehirler)

            # Rota verileri (gidiş ve geliş rotaları)
            rotalar = [
                (1, 2, 350, 4, 1),  # İstanbul -> Ankara
                (2, 1, 350, 4, 1),  # Ankara -> İstanbul
                (2, 3, 500, 6, 1),  # Ankara -> İzmir
                (3, 2, 500, 6, 1),  # İzmir -> Ankara
                (3, 4, 350, 5, 1),  # İzmir -> Antalya
                (4, 3, 350, 5, 1),  # Antalya -> İzmir
                (4, 5, 250, 3, 1),  # Antalya -> Bodrum
                (5, 4, 250, 3, 1),  # Bodrum -> Antalya
                (5, 1, 400, 5, 1),  # Bodrum -> İstanbul
                (1, 5, 400, 5, 1)   # İstanbul -> Bodrum
            ]


            self.cursor.executemany('INSERT INTO oteller (ad, puan, alan, fiyat, il, fotograf) VALUES (?, ?, ?, ?, ?, ?)', oteller)
            self.cursor.executemany('INSERT INTO rotalar (baslangicID, varisID, mesafe, aracsure, ucaksure) VALUES (?, ?, ?, ?, ?)', rotalar)
            self.cursor.execute("INSERT INTO kullanicilar (kullaniciadi, sifre, ad, soyad, telefon) VALUES ('enes', '123', 'Enes', 'Biçici', '5323184256')")
            self.connection.commit()

    def query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
    
Veritabani = veritabani('sql.db')
