from utils.veri import File

class Dogrulama:
    """
    Kullanıcı giriş işlemleri için sınıf.
    """
    @staticmethod
    def uye_dogrula(file_path, tc_or_isim, sifre):
        data = File.dosya_oku(file_path)
        for kayit in data:
            if (kayit[0] == tc_or_isim or kayit[2] == tc_or_isim) and (kayit[2] == sifre or kayit[3] == sifre):
                return kayit
        return None
