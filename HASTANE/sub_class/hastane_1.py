class Recete:
    """
    Hastalara ait reçetelerin yönetimi.
    """
    receteler = []

    def __init__(self, hasta_tc, ilacAdi, doz, talimat):
        self.__hasta_tc = hasta_tc
        self.__ilacAdi = ilacAdi
        self.__doz = doz
        self.__talimat = talimat
        
    def get_hasta_tc(self):
        return self.__hasta_tc

    def set_hasta_tc(self, yeni_hasta_tc):
        self.__hasta_tc = yeni_hasta_tc

    def get_ilacAdi(self):
        return self.__ilacAdi

    def set_ilacAdi(self, yeni_ilacAdi):
        self.__ilacAdi = yeni_ilacAdi

    def get_doz(self):
        return self.__doz

    def set_doz(self, yeni_doz):
        self.__doz = int(yeni_doz)

    def get_talimat(self):
        return self.__talimat

    def set_talimat(self, yeni_talimat):
        self.__talimat = yeni_talimat

    @classmethod
    def recete_ekle(cls, hasta_tc, ilacAdi, doz, talimat):
        """
        Yeni bir reçete ekler.
        """
        yeni_recete = Recete(hasta_tc, ilacAdi, doz, talimat)
        cls.receteler.append(yeni_recete)
        return True

    @classmethod
    def hasta_receteleri_getir(cls, hasta_tc):
        """
        Belirli bir hastaya ait reçeteleri getirir.
        """
        return [p for p in cls.receteler if p.get_hasta_tc() == hasta_tc]

    @classmethod
    def tum_receteler(cls):
        """
        Tüm reçeteleri döner.
        """
        return cls.receteler
    
from base_class.hastane import Hastane
from sub_class.hastane_2 import Doktor, Randevu

class Personel(Hastane):
    """
    Personel sınıfı, personel bilgileriyle çalışır.
    """
    def __init__(self, isim, __rol, sifre):
        self.__isim = isim
        self.__rol = __rol
        self.__sifre = sifre

    def get_isim(self):
        return self.__isim

    def set_isim(self, yeni_isim):
        self.__isim = yeni_isim

    def get_rol(self):
        return self.__rol

    def set_rol(self, yeni_rol):
        self.__rol = yeni_rol

    def get_sifre(self):
        return self.__sifre

    def set_sifre(self, yeni_sifre):
        self.__sifre = yeni_sifre

    @staticmethod
    def veri_oku():
        with open("data/personel.txt", "r", encoding="utf-8") as file:
            return [acıklama.strip().split(",") for acıklama in file.readlines()]

    @classmethod
    def veri_yaz(cls, data):
        with open("data/personel.txt", "a", encoding="utf-8") as file:
            file.write(",".join(data) + "\n")

    def detayları_görüntüle(self):
        print(f"Personel: {self.__isim} - Görev: {self.__rol}")

    @staticmethod
    def doktor_saat_guncelle(doktor_index, yeni_takvim):
        """
        Doktorun çalışma saatlerini günceller.
        """
        try:
            doktorlar = Doktor.veri_oku()
            if 0 <= doktor_index < len(doktorlar):
                doktorlar[doktor_index][2] = yeni_takvim
                Doktor.veri_guncelle(doktorlar)
                return True
            return False
        except Exception as e:
            print(f"Hata: {e}")
            return False

    @staticmethod
    def randevu_onayla(randevu_id):
        """
        Randevuyu onaylar.
        """
        try:
            randevu_id = int(randevu_id) - 1
            randevular = Randevu.veri_oku()
            if 0 <= randevu_id < len(randevular) and randevular[randevu_id][4] != "Onaylandı":
                randevular[randevu_id][4] = "Onaylandı"
                Randevu.veri_guncelle(randevular)
                return True
            return False
        except ValueError:
            return False

    @staticmethod
    def randevu_iptali(randevu_id):
        """
        Randevuyu iptal eder.
        """
        try:
            randevu_id = int(randevu_id) - 1
            randevular = Randevu.veri_oku()
            if 0 <= randevu_id < len(randevular):
                if randevular[randevu_id][4] in ["İptal Edildi"]:
                    return False
                randevular[randevu_id][4] = "İptal Edildi"
                Randevu.veri_guncelle(randevular)
                return True
            return False
        except ValueError:
            return False
