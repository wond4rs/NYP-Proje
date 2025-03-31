class File:
    """
    Genel dosya okuma, yazma ve güncelleme işlemleri için yardımcı sınıf.
    """
    @staticmethod
    def dosya_oku(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return [acıklama.strip().split(",") for acıklama in file.readlines()]
        except FileNotFoundError:
            return []

    @staticmethod
    def dosya_yaz(file_path, data, append=True):
        mode = "a" if append else "w"
        with open(file_path, mode, encoding="utf-8") as file:
            if isinstance(data, list):
                file.write(",".join(data) + "\n")
            else:
                file.write(data + "\n")

    @staticmethod
    def dosya_guncelle(file_path, uptarihd_data):
        with open(file_path, "w", encoding="utf-8") as file:
            for data in uptarihd_data:
                file.write(",".join(data) + "\n")
