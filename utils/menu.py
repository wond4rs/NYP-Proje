from datetime import timedelta
from sub_class.hastane_1 import Personel, Recete
from sub_class.hastane_2 import Doktor, Finans, Randevu
from sub_class.hastane_3 import CovidSonuclari, Hasta, TahlilSonuclari
from utils.dogrulama import Dogrulama
from colorama import Fore, Back, init
init(autoreset=True)

class Menu:
    """
    Metin tabanlı kullanıcı menüsü işlemleri.
    """

    @staticmethod
    def ana_menu():
        while True:
            print(Fore.CYAN+Back.WHITE+"\n--- HASTANE YÖNETİM SİSTEMİ ---")
            print(Fore.CYAN+"1. Hasta Paneli")
            print(Fore.CYAN+"2. Personel Paneli")
            print(Fore.CYAN+"3. Çıkış")
            secim =input("Seçiminizi yapın (1-3): ")

            if secim == "1":
                Menu.hasta_panel()
            elif secim == "2":
                Menu.personel_panel()
            elif secim == "3":
                print("Çıkış yapılıyor...")
                break
            else:
                print(Fore.RED+"Hatalı seçim! Lütfen tekrar deneyin.")

    @staticmethod
    def hasta_panel():
        tc = input("TC Kimlik Numaranızı Girin: ")
        if not (tc.isdigit() and len(tc) == 11):
            print(Fore.RED+"Geçersiz TC Kimlik Numarası! TC 11 haneli ve sadece rakamlardan oluşmalıdır.")
            return
        sifre = input("Şifrenizi Girin: ")
        kullanici = Dogrulama.uye_dogrula("data/hastalar.txt", tc, sifre)

        if kullanici:
            hasta = Hasta(kullanici[0], kullanici[1], kullanici[2], kullanici[3], kullanici[4])
            while True:
                print(Fore.RED+f"\nHoşgeldiniz {hasta.get_isim()} ")
                print(Fore.CYAN+Back.WHITE+"\n--- HASTA PANELİ ---")
                print(Fore.CYAN+"1. Randevu Al")
                print(Fore.CYAN+"2. Randevu İptal Et")
                print(Fore.CYAN+"3. Mevcut Randevular")
                print(Fore.CYAN+"4. Tıbbi Geçmiş")
                print(Fore.CYAN+"5. Tahlil Sonuçları")
                print(Fore.CYAN+"6. Reçetelerim")
                print(Fore.CYAN+"7. Covid-19 Bilgilerim")
                print(Fore.CYAN+"8. Finansal Bilgilerim")
                print(Fore.CYAN+"9. Çıkış")
                secim = input("Seçiminizi yapın (1-9): ")

                from datetime import datetime

                if secim == "1":
                    try:
                        doktorlar = Doktor.veri_oku()
                        print(Fore.GREEN+"Mevcut doktorlar ve çalışma saatleri:")
                        for i, doktor in enumerate(doktorlar, 1):
                            print(f"ID: {i}, Ad: {doktor[0]}, Branş: {doktor[1]}, Çalışma Saatleri: {doktor[2]}")

                        while True:
                            try:
                                doktor_id = int((input("Doktor ID Girin: ")))
                                if 1 <= doktor_id <= len(doktorlar):
                                    break
                                else:
                                    print(Fore.RED+"Geçersiz doktor ID. Lütfen listede bulunan ID'lerden birini girin.")
                            except ValueError:
                                print("Lütfen sadece rakam girin.")
                                

                        while True:
                            tarih = (input("Tarih (YYYY-MM-DD): "))
                            try:
                                datetime.strptime(tarih, "%Y-%m-%d")
                                break
                            except ValueError:
                                print(Fore.RED+"Geçersiz tarih formatı. Lütfen 'YYYY-MM-DD' formatında bir tarih girin.")

                        while True:
                            saat = input("Saat (HH:MM): ")
                            try:
                                datetime.strptime(saat, "%H:%M")
                                break
                            except ValueError:
                                print(Fore.RED+"Geçersiz saat formatı. Lütfen 'HH:MM' formatında bir saat girin.")

                        hasta.randevu_al(doktor_id, tarih, saat)

                    except Exception as e:
                        print(f"Bir hata oluştu: {e}")

                elif secim == "2":
                    hasta.randevular()
                    randevu_id = input("İptal etmek istediğiniz randevunun ID'sini girin: ")
                    if hasta.randevu_iptali(randevu_id):
                        print("Randevu başarıyla iptal edildi.")
                    else:
                        print("Randevu iptal edilemedi. Geçersiz ID, zaten iptal edilmiş olabilir veya sistem hatası.")
                elif secim == "3":
                    hasta.randevular()
                elif secim == "4":
                    print(f"Tıbbi Geçmiş: {hasta.get_tibbi_gecmis()}")
                elif secim == "5":
                    test_sonuclari = TahlilSonuclari.tc_ile_sonuc_getir(tc)
                    if test_sonuclari:
                        print("\nTahlil Sonuçlarınız:")
                        for i, test_sonucu in enumerate(test_sonuclari, 1):
                            print(f"{i}. Test: {test_sonucu[1]}, Sonuç: {test_sonucu[2]}, Tarih: {test_sonucu[3]}")
                    else:
                        print("kayitlı bir tahlil sonucunuz bulunmamaktadır.")
                elif secim == "6":
                    receteler = Recete.hasta_receteleri_getir(tc)
                    if receteler:
                        print("\nReçeteleriniz:")
                        for i, recete in enumerate(receteler, 1):
                            print(f"{i}. İlaç Adı: {recete.get_ilacAdi()}, "
                                f"Talimat: {recete.get_talimat()}, "
                                f"Doz: {recete.get_doz()}")
                    else:
                        print("kayitlı bir reçeteniz bulunmamaktadır.")
                elif secim == "7":
                    test_sonuclari = CovidSonuclari.tc_ile_sonuc_getir(tc)
                    if test_sonuclari:
                        print("\nCovid Sonuçlarınız:")
                        for i, test_sonucu in enumerate(test_sonuclari, 1):
                            print(f"{i}.  Sonuç: {test_sonucu[1]}, Tarih: {test_sonucu[2]}")
                    else:
                        print("kayitlı bir Covid Testi sonucunuz bulunmamaktadır.")
                elif secim == "8":
                    finansIslemleri = Finans.islemleri_goruntule(tc)
                    if finansIslemleri:
                        print("\n--- Finansal İşlemleriniz ---")
                        for t in finansIslemleri:
                            print(f"Tarih: {t[0]}, Tutar: {t[1]}, Açıklama: {t[2]}")
                    else:
                        print("Henüz finansal işlem kaydınız bulunmamaktadır.")
                elif secim == "9":
                    break
                else:
                    print(Fore.RED+"Hatalı seçim! Lütfen tekrar deneyin.")
        else:
            while True:
                    try:
                        secim = input("Üye bulunamadı, kayıt olmak ister misiniz? (Evet-Hayır): ").capitalize()
                        if secim not in ["Evet", "Hayır"]:
                            raise ValueError("Lütfen sadece 'Evet' ya da 'Hayır' seçeneklerinden birini girin.")
                    except ValueError as e:
                        print(e)
                        continue

                    if secim == "Evet":
                        while True:
                            try:
                                yas = input("Yaşınızı girin: ")
                                if not yas.isdigit():
                                    raise ValueError("Lütfen sadece rakam giriniz.")
                                yas = int(yas)
                                break
                            except ValueError as e:
                                print(e)

                        if yas < 18:
                            print("Yaşınız 18'den küçük olduğundan dolayı sadece veliniz size hesap açabilir.")
                            while True:
                                try:
                                    secim = input("Çocuğunuza hesap açmak ister misiniz? (Evet-Hayır): ").capitalize()
                                    if secim not in ["Evet", "Hayır"]:
                                        raise ValueError("Lütfen sadece 'Evet' ya da 'Hayır' seçeneklerinden birini girin.")
                                except ValueError as e:
                                    print(e)
                                    continue

                                if secim == "Evet":
                                    ebeveynName = input("Ebeveyn Adını Girin: ")
                                    ebeveynSoyad = input("Ebeveyn Soyadını Girin: ")
                                    while True:
                                        ebeveynTC = input("Ebeveyn TC kimlik numaranızı girin: ")
                                        if not (ebeveynTC.isdigit() and len(ebeveynTC) == 11):
                                            print(Fore.RED+"Geçersiz TC Kimlik Numarası! TC 11 haneli ve sadece rakamlardan oluşmalıdır.")
                                        else:
                                            break

                                    hastalar = Hasta.veri_oku()
                                    bulundu = False
                                    for hasta in hastalar:
                                        if hasta[0] == ebeveynName and hasta[1] == ebeveynSoyad and hasta[2] == ebeveynTC:
                                            bulundu = True
                                            break

                                    if bulundu:
                                        while True:
                                            try:
                                                secim = input("Ebeveyn bilgileri sistemimizde bulundu. Çocuğunuza hesap açmak ister misiniz? (Evet-Hayır): ").capitalize()
                                                if secim not in ["Evet", "Hayır"]:
                                                    raise ValueError("Lütfen sadece 'Evet' ya da 'Hayır' seçeneklerinden birini girin.")
                                            except ValueError as e:
                                                print(e)
                                                continue

                                            if secim == "Evet":
                                                isim = input("Çocuğunuzun Adını girin: ")
                                                soyad = input("Çocuğunuzun Soyadını girin: ")
                                                while True:
                                                    tc = input("Çocuğunuzun TC kimlik numarasını girin: ")
                                                    if not (tc.isdigit() and len(tc) == 11):
                                                        print(Fore.RED+"Geçersiz TC Kimlik Numarası! TC 11 haneli ve sadece rakamlardan oluşmalıdır.")
                                                    else:
                                                        break
                                                sifre = input("Çocuğunuzun Hesap Şifresini girin: ")
                                                tibbi_gecmis = input("Tıbbi geçmişiniz varsa tıbbi geçmişinizi girin: ")
                                                yeni_hasta = [isim, soyad, tc, sifre, tibbi_gecmis]
                                                if Hasta.hasta_ekle(yeni_hasta):
                                                    print("Yeni hasta başarıyla oluşturuldu.")
                                                else:
                                                    print("Yeni hasta oluşturulamadı. Hata meydana geldi.")
                                                break
                                            elif secim == "Hayır":
                                                print('Ana menüye döndürülüyorsunuz!')
                                                Menu.ana_menu()
                                                break
                                        break
                                    else:
                                        while True:
                                            try:
                                                secim = input("Hastanemize kayıtlı değilsiniz. Hesap açmak ister misiniz? (Evet-Hayır): ").capitalize()
                                                if secim not in ["Evet", "Hayır"]:
                                                    raise ValueError("Lütfen sadece 'Evet' ya da 'Hayır' seçeneklerinden birini girin.")
                                            except ValueError as e:
                                                print(e)
                                                continue

                                            if secim == "Evet":
                                                isim = input("Adınızı girin: ")
                                                soyad = input("Soyadınızı girin: ")
                                                while True:
                                                    tc = input("TC kimlik numaranızı girin: ")
                                                    if not (tc.isdigit() and len(tc) == 11):
                                                        print(Fore.RED+"Geçersiz TC Kimlik Numarası! TC 11 haneli ve sadece rakamlardan oluşmalıdır.")
                                                    else:
                                                        break
                                                sifre = input("Şifrenizi girin: ")
                                                tibbi_gecmis = input("Tıbbi geçmişiniz varsa tıbbi geçmişinizi girin: ")
                                                yeni_hasta = [isim, soyad, tc, sifre, tibbi_gecmis]
                                                if Hasta.hasta_ekle(yeni_hasta):
                                                    print("Kaydınız başarıyla oluşturuldu.")
                                                else:
                                                    print("Kaydınız oluşturulamadı. Hata meydana geldi.")
                                                break
                                        print('Ana menüye döndürülüyorsunuz!')
                                        Menu.ana_menu()
                                        break
                                elif secim == "Hayır":
                                    print('Ana menüye döndürülüyorsunuz!')
                                    Menu.ana_menu()
                                    break

                        isim = input("Adınızı girin: ")
                        soyad = input("Soyadınızı girin: ")
                        while True:
                            tc = input("TC kimlik numaranızı girin: ")
                            if not (tc.isdigit() and len(tc) == 11):
                                print(Fore.RED+"Geçersiz TC Kimlik Numarası! TC 11 haneli ve sadece rakamlardan oluşmalıdır.")
                            else:
                                break
                        sifre = input("Şifrenizi girin: ")
                        tibbi_gecmis = input("Tıbbi geçmişiniz varsa tıbbi geçmişinizi girin: ")
                        yeni_hasta = [isim, soyad, tc, sifre, tibbi_gecmis]
                        if Hasta.hasta_ekle(yeni_hasta):
                            print("Yeni hasta başarıyla oluşturuldu.")
                        else:
                            print("Yeni hasta oluşturulamadı. Hata meydana geldi.")
                    else:
                        print('Ana menüye döndürülüyorsunuz!')
                        Menu.ana_menu()
                        break
    @staticmethod
    def personel_panel():
        isim = input("Adınızı Girin: ")
        sifre = input("Şifrenizi Girin: ")
        kullanici = Dogrulama.uye_dogrula("data/personel.txt", isim, sifre)

        if kullanici:
            yetkili = Personel(kullanici[0], kullanici[1], kullanici[2])
            while True:
                print(Fore.RED+f"\nHoşgeldiniz {yetkili.get_rol()} {yetkili.get_isim()}")
                print(Fore.CYAN+Back.WHITE+"--- PERSONEL PANELİ ---")
                print(Fore.CYAN+"1. Doktor Takvim Yönetimi")
                print(Fore.CYAN+"2. Randevuları Yönet")
                print(Fore.CYAN+"3. Hasta Yönetim Menüsü")
                print(Fore.CYAN+"4. Tahlil Sonuçları Yönet")
                print(Fore.CYAN+"5. Reçete Yönetimi")
                print(Fore.CYAN+"6. Covid Sonuçları Yönetimi")
                print(Fore.CYAN+"7. Finans Yönetimi")
                print(Fore.CYAN+"8. Çıkış")
                secim = input("Seçiminizi yapın (1-8): ")

                if secim == "1":
                    doktorlar = Doktor.veri_oku()
                    print(Fore.GREEN+"Mevcut doktorlar ve çalışma saatleri:")
                    for i, doktor in enumerate(doktorlar, 1):
                        print(f"ID: {i}, Ad: {doktor[0]}, Branş: {doktor[1]}, Çalışma Saatleri: {doktor[2]}")

                    doktor_id = input("Takvimini yönetmek istediğiniz doktorun ID'sini girin: ")
                    if doktor_id.isdigit() and 1 <= int(doktor_id) <= len(doktorlar):
                        doktor_secimi = doktorlar[int(doktor_id) - 1]
                        print(f"Seçilen Doktor: {doktor_secimi[0]}, Branş: {doktor_secimi[1]}")
                        print("1. Çalışma Saatlerini Görüntüle")
                        print("2. Çalışma Saatlerini Güncelle")
                        secenek = input("Seçiminizi yapın (1-2): ")

                        if secenek == "1":
                            print(f"{doktor_secimi[0]} Çalışma Saatleri: {doktor_secimi[2]}")
                        elif secenek == "2":
                            from datetime import datetime
                            while True:
                                yeni_takvim = input(f"{doktor_secimi[0]} için yeni çalışma saatlerini girin (örn. 09:00-17:00): ")  
                                try:
                                    baslangic,bitis=yeni_takvim.split("-")
                                    baslangic=datetime.strptime(baslangic,"%H:%M")
                                    bitis =datetime.strptime(bitis,"%H:%M")
                                    break
                                except  ValueError:
                                    print(Fore.RED+"Geçersiz saat formati lütfen belirtilen formatta giriniz.")
                                    
                            if Personel.doktor_saat_guncelle(int(doktor_id) - 1, yeni_takvim):
                                print("Çalışma saatleri başarıyla güncellendi.")
                            else:
                                print("Çalışma saatleri güncellenemedi.")
                        else:
                            print(Fore.RED+"Geçersiz seçim!")
                    else:
                        print(Fore.RED+"Geçersiz doktor ID'si!")
                elif secim == "2":
                    randevular = Randevu.veri_oku()
                    print(Fore.GREEN+"Mevcut randevular:")
                    for i, randevu in enumerate(randevular, 1):
                        print(f"ID: {i}, Hasta: {randevu[0]}, Doktor: {randevu[1]}, Tarih: {randevu[2]}, Saat: {randevu[3]}, Durum: {randevu[4]}")

                    randevu_id = input("Yönetmek istediğiniz randevunun ID'sini girin: ")
                    print("\n1. Onayla")
                    print("2. İptal Et")
                    secenek = input("Seçiminizi yapın (1-2): ")

                    if secenek == "1":
                        if Personel.randevu_onayla(randevu_id):
                            print("Randevu başarıyla onaylandı.")
                        else:
                            print("Randevu onaylama onaylanamadı veya Randevu zaten onaylanmış olabilir.")
                    elif secenek == "2":
                        if Personel.randevu_iptali(randevu_id):
                            print("Randevu başarıyla iptal edildi.")
                        else:
                            print("Randevu iptal edilemedi veya Randevu zaten iptal edilmiş olabilir.")
                    else:
                        print(Fore.RED+"Geçersiz seçim!")
                elif secim == "3":
                    print(Fore.GREEN+"\nHasta Yönetim Menüsü:")
                    print("1. Tüm Hastaları Gör")
                    print("2. Yeni Hasta Oluştur")
                    print("3. Hasta Sil")
                    secenek = input("Seçiminizi yapın (1-3): ")

                    if secenek == "1":
                        hastalar = Hasta.veri_oku()
                        print(Fore.GREEN+"\nMevcut Hastalar:")
                        for i, p in enumerate(hastalar, 1):
                            print(f"ID: {i}, Hasta: {p[0]} {p[1]} - TC: {p[2]}")
                    elif secenek == "2":
                        isim = input("Yeni hastanın adını girin: ")
                        soyad = input("Yeni hastanın soyadını girin: ")
                        tc = input("Yeni hastanın TC kimlik numarasını girin: ")
                        if not (tc.isdigit() and len(tc) == 11):
                                print(Fore.RED+"Geçersiz TC Kimlik Numarası! TC 11 haneli ve sadece rakamlardan oluşmalıdır.")
                                return
                        sifre = input("Yeni hastanın şifresini girin: ")
                        tibbi_gecmis = input("Yeni hastanın tıbbi geçmişini girin: ")

                        yeni_hasta = [isim, soyad, tc, sifre, tibbi_gecmis]
                        if Hasta.hasta_ekle(yeni_hasta):
                            print("Yeni hasta başarıyla oluşturuldu.")
                        else:
                            print("Yeni hasta oluşturulamadı. Hata meydana geldi.")
                    elif secenek == "3":
                        hastalar = Hasta.veri_oku()
                        print(Fore.GREEN+"\nMevcut Hastalar:")
                        for i, p in enumerate(hastalar, 1):
                            print(f"ID: {i}, Hasta: {p[0]} {p[1]} - TC: {p[2]}")
                        hasta_id = input("Silmek istediğiniz hastanın ID'sini girin: ")

                        if hasta_id.isdigit() and 1 <= int(hasta_id) <= len(hastalar):
                            if Hasta.hasta_sil(int(hasta_id) - 1):
                                print("Hasta başarıyla silindi.")
                            else:
                                print("Hasta silinemedi. Hata meydana geldi.")
                        else:
                            print(Fore.RED+"Geçersiz hasta ID'si!")
                    else:
                        print(Fore.RED+"Geçersiz seçim!")
                elif secim == "4":
                    print(Fore.GREEN+"\n--- TAHLİL SONUÇLARI YÖNETİMİ ---")
                    hastalar = Hasta.veri_oku()
                    print(Fore.GREEN+"Mevcut Hastalar:")
                    for i, p in enumerate(hastalar, 1):
                        print(f"ID: {i}, Hasta: {p[0]} {p[1]} - TC: {p[2]}")
                    hasta_id = input("Tahlil sonucu eklemek istediğiniz hastanın ID'sini girin: ")

                    if hasta_id.isdigit() and 1 <= int(hasta_id) <= len(hastalar):
                        tc = hastalar[int(hasta_id) - 1][2]
                        test_isim = input("Test adını girin: ")
                        test_sonucu = input("Test sonucunu girin: ")

                        if TahlilSonuclari.sonuc_ekle(tc, test_isim, test_sonucu):
                            print("Tahlil sonucu başarıyla eklendi.")
                        else:
                            print("Tahlil sonucu eklenirken bir hata oluştu.")
                    else:
                        print(Fore.RED+"Geçersiz hasta ID'si!")
                elif secim == "5":
                    print(Fore.GREEN+"\n--- REÇETE YÖNETİMİ ---")
                    hastalar = Hasta.veri_oku()
                    print(Fore.GREEN+"Mevcut Hastalar:")
                    for i, p in enumerate(hastalar, 1):
                        print(f"ID: {i}, Hasta: {p[0]} {p[1]} - TC: {p[2]}")
                    hasta_id = input("Reçete yazmak istediğiniz hastanın ID'sini girin: ")

                    if hasta_id.isdigit() and 1 <= int(hasta_id) <= len(hastalar):
                        tc = hastalar[int(hasta_id) - 1][2]
                        ilac = input("İlaç adını girin: ")
                        doz = input("Doz bilgisini girin: ")
                        talimat = input("Talimatları girin: ")

                        if Recete.recete_ekle(tc, ilac, doz, talimat):
                            print("Reçete başarıyla eklendi.")
                        else:
                            print("Reçete eklenirken bir hata oluştu.")
                    else:
                        print(Fore.RED+"Geçersiz hasta ID'si!")
                elif secim == "6":
                    print(Fore.GREEN+"\n--- COVİD SONUÇLARI YÖNETİMİ ---")
                    hastalar = Hasta.veri_oku()
                    print(Fore.GREEN+"Mevcut Hastalar:")
                    for i, p in enumerate(hastalar, 1):
                        print(f"ID: {i}, Hasta: {p[0]} {p[1]} - TC: {p[2]}")
                    hasta_id = input("Covid sonucu eklemek istediğiniz hastanın ID'sini girin: ")

                    if hasta_id.isdigit() and 1 <= int(hasta_id) <= len(hastalar):
                        tc = hastalar[int(hasta_id) - 1][2]
                        test_sonucu = input("Test sonucunu girin (POZİTİF-NEGATİF): ")
                        son_covid_tarihi = CovidSonuclari.tc_ile_sonuc_getir(tc)

                        if son_covid_tarihi and len(son_covid_tarihi) > 3 and isinstance(son_covid_tarihi[3], datetime):
                            test_tarihi = son_covid_tarihi[3]
                        else:
                            from datetime import datetime
                            test_tarihi = datetime.min

                        on_bes_gün_sonra = test_tarihi + timedelta(days=15)

                        if datetime.now() < on_bes_gün_sonra:
                            print('15 Gün Geçmeden Yeni Test Sonucu Ekleyemezsin!')
                            secenek = input('Test Sonucu Acil Eklenmelimi?: ')

                            if secenek.capitalize() == 'Evet':
                                isim = input("Adınızı Girin: ")
                                sifre = input("Şifrenizi Girin: ")
                                gecerliKullanici = Dogrulama.uye_dogrula("data/personel.txt", isim, sifre)
                                if gecerliKullanici:
                                    if CovidSonuclari.sonuc_ekle(tc, 'CORONA', test_sonucu):
                                        print("Covid sonucu başarıyla eklendi.")
                                    else:
                                        print("Covid sonucu eklenirken bir hata oluştu.")
                                else:
                                    print("Geçersiz personel bilgileri!")
                            else:
                                print('15 gün sonra test sonucu ekleyebilirsiniz')
                        else:
                            if CovidSonuclari.sonuc_ekle(tc, 'CORONA', test_sonucu):
                                print("Covid sonucu başarıyla eklendi.")
                            else:
                                print("Covid sonucu eklenirken bir hata oluştu.")
                    else:
                        print(Fore.RED+"Geçersiz hasta ID'si!")
                elif secim == "7":
                    print(Fore.GREEN+"\n--- FİNANS YÖNETİMİ ---")
                    print("1. Ödeme Al")
                    print("2. Tüm İşlemleri Görüntüle")
                    print("3. Borç Raporu Oluştur")
                    secenek = input("Seçiminizi yapın (1-3): ")

                    if secenek == "1":
                        hastalar = Hasta.veri_oku()
                        print(Fore.GREEN+"Mevcut Hastalar:")
                        for i, p in enumerate(hastalar, 1):
                            print(f"ID: {i}, Hasta: {p[0]} {p[1]} - TC: {p[2]}")
                        hasta_id = input("Ödeme almak istediğiniz hastanın ID'sini girin: ")

                        if hasta_id.isdigit() and 1 <= int(hasta_id) <= len(hastalar):
                            tc = hastalar[int(hasta_id) - 1][2]
                            adet = input("Ödeme tutarını girin: ")
                            aciklama = input("Ödeme açıklamasını girin: ")
                            if Finans.islem_ekle(tc, adet, aciklama):
                                print("Ödeme başarıyla kaydedildi.")
                            else:
                                print("Ödeme kaydedilemedi.")
                        else:
                            print(Fore.RED+"Geçersiz hasta ID'si!")
                    elif secenek == "2":
                        islem = Finans.islemleri_goruntule()
                        if islem:
                            print("\n--- Tüm Finansal İşlemler ---")
                            for t in islem:
                                print(f"TC: {t[0]}, Tutar: {t[1]}, Açıklama: {t[2]}")
                        else:
                            print("kayitlı finansal işlem bulunmamaktadır.")
                    elif secenek == "3":
                        kullanici_id = input("Kullanıcı TC'nizi girin: ").strip()
                        print("Borç raporu oluşturuluyor...")
                        Finans.borclari_raporla(kullanici_id)
                    else:
                        print(Fore.RED+"Geçersiz seçim!")
                elif secim == "8":
                    break
                else:
                    print(Fore.RED+"Hatalı seçim! Lütfen tekrar deneyin.")
        else:
            print(Fore.RED+"Ad veya Şifre hatalı!")