from datetime import datetime

# Türkçe ve İngilizce ay isimlerini içeren bir sözlük
__ay_isimleri = {
    'Oca': '01',
    'Şub': '02',
    'Mar': '03',
    'Nis': '04',
    'May': '05',
    'Haz': '06',
    'Tem': '07',
    'Ağu': '08',
    'Eyl': '09',
    'Eki': '10',
    'Kas': '11',
    'Ara': '12'
}


def __turkce_tarih_cevir(saat_verisi):
    # Türkçe ay isimlerini İngilizceye çevirme
    for tr_ay, en_ay in __ay_isimleri.items():
        saat_verisi = saat_verisi.replace(tr_ay, en_ay)
    # "ÖÖ" ifadesini kaldırma ve "AÖ" ifadesini "PM" ile değiştirme
    saat_verisi = saat_verisi.replace('ÖÖ', 'AM').replace('ÖS', 'PM')
    # "・" karakterini kaldırma
    saat_verisi = saat_verisi.replace('・', ' ')
    return saat_verisi.strip().split(' ')  # Boşluk karakterlerini temizleme


def converToDateTime(saat):
    formatted_saat = __turkce_tarih_cevir(saat)
    dilim = formatted_saat[0]
    saat = formatted_saat[1]
    del formatted_saat[0]
    del formatted_saat[0]
    tersten = '-'.join(map(str, formatted_saat[::-1]))
    dateTime1 = tersten + " " + saat + " " + dilim
    return datetime.strptime(dateTime1, "%Y-%m-%d %I:%M %p")
