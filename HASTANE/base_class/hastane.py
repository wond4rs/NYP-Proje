from abc import ABC, abstractmethod

class Hastane(ABC):
    """
    Hastane sınıfı, tüm alt sınıflar için bir şablon sağlar.
    """

    @staticmethod
    @abstractmethod
    def veri_oku():
        """Dosyadan veri okuma işlemi."""
        pass

    @classmethod
    @abstractmethod
    def veri_yaz(cls, data):
        """Dosyaya veri yazma işlemi."""
        pass

    @abstractmethod
    def detayları_görüntüle(self):
        """Nesne detaylarını görüntüleme."""
        pass
