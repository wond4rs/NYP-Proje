from base_class.hastane import Hastane
from sub_class.hastane_2 import Randevu
from utils.veri import File

class Hasta(Hastane):
    """
    Hasta sınıfı, hasta bilgileriyle çalışır.
    """
    def __init__(self, isim, soyad, tc, sifre, tibbi_gecmis):
        self.__isim = isim
        self.__soyad = soyad
        self.__tc = tc
        self.__sifre = sifre
        self.__tibbi_gecmis = tibbi_gecmis

    def get_isim(self):
        return self.__isim

    def set_isim(self, yeni_isim):
        self.__isim = yeni_isim

    def get_soyad(self):
        return self.__soyad

    def set_soyad(self, yeni_soyad):
        self.__soyad = yeni_soyad

    def get_tc(self):
        return self.__tc

    def set_tc(self, yeni_tc):
        self.__tc = yeni_tc

    def get_sifre(self):
        return self.__sifre

    def set_sifre(self, yeni_sifre):
        self.__sifre = yeni_sifre

    def get_tibbi_gecmis(self):
        return self.__tibbi_gecmis

    def set_tibbi_gecmis(self, yeni_tibbi_gecmis):
        self.__tibbi_gecmis = yeni_tibbi_gecmis

    @staticmethod
    def veri_oku():
        with open("data/hastalar.txt", "r", encoding="utf-8") as file:
            return [acıklama.strip().split(",") for acıklama in file.readlines()]

    @classmethod
    def veri_yaz(cls, data):
        with open("data/hastalar.txt", "a", encoding="utf-8") as file:
            file.write(",".join(data) + "\n")

    def detayları_görüntüle(self):
        print(f"Hasta: {self.__isim} {self.__soyad} - TC: {self.__tc} - Tıbbi Geçmiş: {self.__tibbi_gecmis}")

    def randevu_al(self, doktor_id, tarih, saat):
        Randevu.veri_yaz([self.__tc, doktor_id, tarih, saat, "Beklemede"])
        print(f"Randevu başarıyla alındı: {tarih} {saat} - Doktor ID: {doktor_id}")

    def randevular(self):
        """
        Hastanın mevcut randevularını görüntüler.
        """
        randevular = Randevu.veri_oku()
        print(f"{self.__isim} {self.__soyad} için mevcut randevular:")
        for i, randevu in enumerate(randevular, 1):
            if randevu[0] == self.__tc:
                if randevu[4] in ["İptal Edildi", "Onaylandı"]:
                    continue
                print(f"ID: {i}, Doktor: {randevu[1]}, Tarih: {randevu[2]}, Saat: {randevu[3]}, Durum: {randevu[4]}")

    def randevu_iptali(self, randevu_id):
        """
        Randevuyu iptal eder.
        """
        try:
            randevu_id = int(randevu_id) - 1
            randevular = Randevu.veri_oku()
            if 0 <= randevu_id < len(randevular) and randevular[randevu_id][0] == self.__tc:
                if randevular[randevu_id][4] in ["İptal Edildi", "Onaylandı"]:
                    return False
                randevular[randevu_id][4] = "İptal Edildi"
                Randevu.veri_guncelle(randevular)
                return True
            return False
        except ValueError:
            return False
        
    @staticmethod
    def hasta_ekle(yeni_hasta):
        """
        Yeni bir hasta ekler.
        """
        try:
            hastalar = Hasta.veri_oku()
            hastalar.append(yeni_hasta)
            Hasta.veri_guncelle(hastalar)
            return True
        except Exception as e:
            print(f"Hata: {e}")
            return False

    @staticmethod
    def hasta_sil(hasta_index):
        """
        Bir hastayı siler.
        """
        try:
            hastalar = Hasta.veri_oku()
            if 0 <= hasta_index < len(hastalar):
                del hastalar[hasta_index]
                Hasta.veri_guncelle(hastalar)
                return True
            return False
        except Exception as e:
            print(f"Hata: {e}")
            return False

    @staticmethod
    def veri_guncelle(data):
        """
        Hasta dosyasını günceller.
        """
        File.dosya_guncelle("data/hastalar.txt", data)

import datetime
import os

class TahlilSonuclari:
    """
    Tahlil sonuçlarını yönetmek için bir sınıf.
    Tahlil sonuçları 'tests.txt' dosyasında saklanır.
    """
    @staticmethod
    def sonuclari_getir():
        """
        Tahlil sonuçlarını dosyadan okur ve bir liste olarak döner.)
        """
        if not os.path.exists("data/tests.txt"):
            return []
        with open("data/tests.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [acıklama.strip().split("|") for acıklama in lines]

    @staticmethod
    def sonuc_ekle(tc, test_type, test_sonucu):
        """
        Yeni bir tahlil sonucunu dosyaya ekler.
        True (başarılı), False (başarısız)
        """
        try:
            suanki_saat = datetime.datetime.now()
            with open("data/tests.txt", "a", encoding="utf-8") as file:
                file.write(f"{tc}|{test_type}|{test_sonucu}|{suanki_saat}\n")
            return True
        except Exception as e:
            print(f"Hata: {e}")
            return False

    @staticmethod
    def tc_ile_sonuc_getir(tc):
        """
        Belirli bir TC Kimlik Numarasına ait tahlil sonuçlarını döner.
        """
        test_sonucuclari = TahlilSonuclari.sonuclari_getir()
        return [test_sonucu for test_sonucu in test_sonucuclari if test_sonucu[0] == tc]

class CovidSonuclari:
    """
    Covid sonuçlarını yönetmek için bir sınıf.
    Covid sonuçları 'covid_test_sonuclari.txt' dosyasında saklanır.
    """
    @staticmethod
    def sonuclari_getir():
        """
        Covid sonuçlarını dosyadan okur ve bir liste olarak döner.)
        """
        if not os.path.exists("data/covid_test_sonuclari.txt"):
            return []
        with open("data/covid_test_sonuclari.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [acıklama.strip().split("|") for acıklama in lines]

    @staticmethod
    def sonuc_ekle(tc, test, test_sonucu):
        """
        Yeni bir Covid sonucunu dosyaya ekler.
        True (başarılı), False (başarısız)
        """
        try:
            suanki_saat = datetime.datetime.now()
            with open("data/covid_test_sonuclari.txt", "a", encoding="utf-8") as file:
                file.write(f"{tc}|{test}|{test_sonucu}|{suanki_saat}\n")
            return True
        except Exception as e:
            print(f"Hata: {e}")
            return False

    @staticmethod
    def tc_ile_sonuc_getir(tc):
        """
        Belirli bir TC Kimlik Numarasına ait covid sonuçlarını döner.
        """
        test_sonuclari = CovidSonuclari.sonuclari_getir()
        return [test_sonucu for test_sonucu in test_sonuclari if test_sonucu[0] == tc]