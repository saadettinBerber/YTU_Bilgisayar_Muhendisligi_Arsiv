from degiskenler import *
import json
import subprocess
import urllib.parse
import os
def get_git_repo_url():
    current_directory = os.getcwd()
    py_bulamadi = False
    # Mevcut dizinde .py dosyası olduğu sürece üst dizine çık
    while not py_bulamadi:
        # Eğer mevcut dizinde .py dosyası varsa, döngüyü kır
        for file in os.listdir(current_directory):
            if file.endswith(".py"):
                py_bulamadi = False
                break
            else:
                py_bulamadi = True
        # Bir üst dizine çık
        if not py_bulamadi:
            current_directory = os.path.dirname(current_directory)

        # Eğer en üst dizine ulaşırsa ve hala .py dosyası yoksa, çık
        if current_directory == '/' or current_directory == '':
            return "Python dosyası bulunamadı."

    try:
        # Git reposunun URL'sini al
        git_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], cwd=current_directory)
        return git_url.decode().strip()
    except subprocess.CalledProcessError:
        # Eğer mevcut dizin bir git reposu değilse
        return "Mevcut dizin bir git reposu değil."
def konfigurasyon_json_guncelle(file_path):
    global ANAHTAR_VE_LINKLER
    # Anahtarları kontrol et ve güncelle
    updated = False
    try:
        # JSON dosyasını oku
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {}

        for key, default_link in ANAHTAR_VE_LINKLER.items():
            if key not in data or not isinstance(data[key], str) or not urllib.parse.urlparse(data[key]).scheme:
                data[key] = default_link
                updated = True

        # Eğer güncelleme yapıldıysa, dosyayı yeniden yaz
        if updated:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Konfigurasyon dosyası güncellenirken hata oluştu: {e}")
    return updated
def update_anahtar_ve_degerler(file_path):
    global ANAHTAR_VE_LINKLER
    try:
        # JSON dosyasını oku
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        # Anahtarları kontrol et ve güncelle
        updated = False
        for key, value in ANAHTAR_VE_LINKLER.items():
            # JSON verisinde anahtarı güncelle
            ANAHTAR_VE_LINKLER[key] = json_data.get(key, value)
            updated = True

        # Eğer güncelleme yapıldıysa, dosyayı yeniden yaz
        if updated:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        return f"Hata: {e}"
    
def global_konfigurasyon_degiskenlerini_guncelle():
    global VARSAYILAN_GITHUB_URL, HOCA_YORULMALA_LINKI, HOCA_OYLAMA_LINKI, DERS_YORUMLAMA_LINKI, DERS_OYLAMA_LINKI, DERS_OYLAMA_LINKI_CSV, DERS_YORUMLAMA_LINKI_CSV, HOCA_OYLAMA_LINKI_CSV, HOCA_YORULMALA_LINKI_CSV
    VARSAYILAN_GITHUB_URL = ANAHTAR_VE_LINKLER[GITHUB_URL_ANAHTARI]
    HOCA_YORULMALA_LINKI = ANAHTAR_VE_LINKLER[HOCA_YORUMLAMA_ANAHTARI]
    HOCA_OYLAMA_LINKI = ANAHTAR_VE_LINKLER[HOCA_OYLAMA_ANAHTARI]
    DERS_YORUMLAMA_LINKI = ANAHTAR_VE_LINKLER[DERS_YORUMLAMA_ANAHTARI]
    DERS_OYLAMA_LINKI = ANAHTAR_VE_LINKLER[DERS_OYLAMA_ANAHTARI]
    DERS_OYLAMA_LINKI_CSV = ANAHTAR_VE_LINKLER[DERS_OYLAMA_CSV_ANAHTARI]
    DERS_YORUMLAMA_LINKI_CSV = ANAHTAR_VE_LINKLER[DERS_YORUMLAMA_CSV_ANAHTARI]
    HOCA_OYLAMA_LINKI_CSV = ANAHTAR_VE_LINKLER[HOCA_OYLAMA_CSV_ANAHTARI]
    HOCA_YORULMALA_LINKI_CSV = ANAHTAR_VE_LINKLER[HOCA_YORUMLAMA_CSV_ANAHTARI]

def konfigurasyon_ilklendirme_islemleri(json_file_path):
    # LİNKLERİN TUTULDUĞU VERİELRİ KONTROL EDİP OLMAYAN DEĞERLERİ GÜNCELLEME
    konfigurasyon_json_guncelle(json_file_path)
    update_anahtar_ve_degerler(json_file_path)
    global_konfigurasyon_degiskenlerini_guncelle()