from base_class.hastane import Hastane
from utils.veri import File

class Doktor(Hastane):
    """
    Doktor sınıfı, doktor bilgileriyle çalışır.
    """
    def __init__(self, isim, brans, calisma_saatleri):
        self.__isim = isim
        self.__brans = brans
        self.__calisma_saatleri = calisma_saatleri

    def get_isim(self):
        return self.__isim

    def set_isim(self, yeni_isim):
        self.__isim = yeni_isim

    def get_brans(self):
        return self.__brans

    def set_brans(self, yeni_brans):
        self.__brans = yeni_brans

    def get_calisma_saatleri(self):
        return self.__calisma_saatleri

    def set_calisma_saatleri(self, yeni_saatler):
        self.__calisma_saatleri = yeni_saatler

    @staticmethod
    def veri_oku():
        with open("data/doktorlar.txt", "r", encoding="utf-8") as file:
            return [acıklama.strip().split(",") for acıklama in file.readlines()]

    @classmethod
    def veri_yaz(cls, data):
        with open("data/doktorlar.txt", "a", encoding="utf-8") as file:
            file.write(",".join(data) + "\n")

    def detayları_görüntüle(self):
        print(f"Doktor: {self.__isim} - Branş: {self.__brans} - Çalışma Saatleri: {self.__calisma_saatleri}")

    @staticmethod
    def veri_guncelle(data):
        """
        Doktor dosyasını günceller.
        """
        File.dosya_guncelle("data/doktorlar.txt", data)

from base_class.hastane import Hastane
from utils.veri import File

class Randevu(Hastane):
    """
    Randevu sınıfı, randevu bilgileriyle çalışır.
    """
    def __init__(self, hasta_id, doktor_id, tarih, saat, durum):
        self.__hasta_id = hasta_id
        self.__doktor_id = doktor_id
        self.__tarih = tarih
        self.__saat = saat
        self.__durum = durum

    def get_hasta_id(self):
        return self.__hasta_id

    def set_hasta_id(self, yeni_hasta_id):
        self.__hasta_id = yeni_hasta_id

    def get_doktor_id(self):
        return self.__doktor_id

    def set_doktor_id(self, yeni_doktor_id):
        self.__doktor_id = yeni_doktor_id

    def get_tarih(self):
        return self.__tarih

    def set_tarih(self, yeni_tarih):
        self.__tarih = yeni_tarih

    def get_saat(self):
        return self.__saat

    def set_saat(self, yeni_saat):
        self.__saat = yeni_saat

    def get_durum(self):
        return self.__durum

    def set_durum(self, yeni_durum):
        self.__durum = yeni_durum

    
    @staticmethod
    def veri_oku():
        with open("data/randevular.txt", "r", encoding="utf-8") as file:
            return [list(map(str, acıklama.strip().split(","))) for acıklama in file.readlines()]


    @classmethod
    def veri_yaz(cls, data):
        with open("data/randevular.txt", "a", encoding="utf-8") as file:
            file.write(",".join(map(str, data)) + "\n")


    def detayları_görüntüle(self):
        print(f"Randevu: Hasta ID: {self.__hasta_id} - Doktor ID: {self.__doktor_id} - Tarih: {self.__tarih} - Saat: {self.__saat} - Durum: {self.__durum}")

    @staticmethod
    def veri_guncelle(data):
        """
        Randevu dosyasını günceller.
        """
        File.dosya_guncelle("data/randevular.txt", data)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

class Finans:
    @staticmethod
    def islem_ekle(hasta_tc, adet, aciklama):
        """
        Yeni bir işlem ekler.
        """
        try:
            with open("data/islem.txt", "a") as file:
                file.write(f"{hasta_tc},{adet},{aciklama}\n")
            return True
        except Exception as e:
            print(f"İşlem eklenirken hata oluştu: {e}")
            return False

    @staticmethod
    def islemleri_goruntule(hasta_tc=None):
        """
        Tüm işlemleri veya belirli bir hasta için işlemleri görüntüler.
        """
        try:
            with open("data/islem.txt", "r") as file:
                islem = [acıklama.strip().split(",") for acıklama in file.readlines()]

            if hasta_tc:
                islem = [t for t in islem if t[0] == hasta_tc]

            return islem
        except FileNotFoundError:
            return []

    @staticmethod
    def borclar(kullanici_id):
        """
        Kullanıcının borçlarını islem.txt dosyasından alır.
        """
        try:
            with open("data/islem.txt", "r") as file:
                borclar = []
                for acıklama in file.readlines():
                    hasta_tc, adet, aciklama = acıklama.strip().split(",")
                    if hasta_tc == kullanici_id:
                        borc = {
                            "id": len(borclar) + 1,
                            "kullanici_id": hasta_tc,
                            "adet": float(adet),
                            "tarih": datetime.now().strftime("%Y-%m-%d"),
                            "odenmis": aciklama.lower() == "odenmis"
                        }
                        borclar.append(borc)
                return borclar
        except FileNotFoundError:
            print("Borç dosyası bulunamadı.")
            return []

    @staticmethod
    def borclari_raporla(kullanici_id):
        """
        Kullanıcının borç raporunu oluşturur ve ekranda gösterir.
        """
        borclar = Finans.borclar(kullanici_id)
        if not borclar:
            print("Borç kaydı bulunamadı.")
            return
        
        print("\n--- BORÇ RAPORU ---")
        toplam_borc = 0
        rapor_bilgileri = []
        for borc in borclar:
            durum = "Ödenmemiş" if not borc["odenmis"] else "Ödenmiş"
            acıklama = f"Borç ID: {borc["id"]}, Tutar: {borc["adet"]} TL, Tarih: {borc["tarih"]}, Durum: {durum}"
            rapor_bilgileri.append(acıklama)
            print(acıklama)
            if not borc["odenmis"]:
                toplam_borc += borc["adet"]
        
        print(f"Toplam Borç: {toplam_borc} TL")
        if toplam_borc > 0:
            print("Borç ödeme seçeneklerini görüntülemek için ilgili menüye gidebilirsiniz.")

        save_pdf = input("Bu raporu PDF olarak kaydetmek ister misiniz? (E/H): ").strip().lower()
        if save_pdf == 'e':
            Finans.pdf_donustur(kullanici_id, rapor_bilgileri, toplam_borc)
            print("Rapor PDF olarak kaydedildi.")

    @staticmethod
    def pdf_donustur(kullanici_id, rapor_bilgileri, toplam_borc):
        """
        Borç raporunu PDF formatında kaydeder.
        """
        fileisim = f"borc_raporu_{kullanici_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        c = canvas.Canvas(fileisim, pagesize=letter)
        c.drawString(100, 750, f"BORÇ RAPORU - Kullanıcı ID: {kullanici_id}")
        y_position = 700

        for acıklama in rapor_bilgileri:
            c.drawString(50, y_position, acıklama)
            y_position -= 20

        c.drawString(50, y_position - 20, f"Toplam Borç: {toplam_borc} TL")
        c.save()