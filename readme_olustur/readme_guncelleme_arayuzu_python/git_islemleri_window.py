import sys
import os
import subprocess
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox, QInputDialog, QLineEdit
from degiskenler import *
from progress_dialog import CustomProgressDialog
from threadler import CMDScriptRunnerThread
from PyQt5.QtGui import QIcon
import json
class GitIslemleriWindow(QDialog):
    def __init__(self):
        super(GitIslemleriWindow, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Git İşlemleri")
        self.setMinimumSize(300, 200)
        # Dialog layout
        self.layout = QVBoxLayout()
        if os.path.exists(SELCUKLU_ICO_PATH):
            self.setWindowIcon(QIcon(SELCUKLU_ICO_PATH))

        # Butonlar ve renkler
        self.buttons = [
            QPushButton("Google Form Güncelle"),
            QPushButton("Readme Güncelle"),
            QPushButton("Değişiklikleri Github'a Pushla"),
            QPushButton("Arayüz Kodlarını Güncelle"),
            QPushButton("Rutin Kontrolü Başlat")
        ]

        self.colors = [
            "background-color: #C0392B; color: white;",  # Kırmızı
            "background-color: #27AE60; color: white;",  # Yeşil
            "background-color: #1ABC9C; color: white;",  # Açık Mavi/Turkuaz
            "background-color: #F1C40F; color: black;",  # Sarı
            "background-color: #FF69B4; color: white;"   # Pembe
        ]


        # Buton fonksiyonları
        self.functions = [
            self.update_google_form,
            self.update_readme,
            self.push_changes,
            self.update_interface,
            self.start_routine_check
        ]
        # Butonları dialog'a ekleme, renklendirme ve bağlama
        for btn, color, func in zip(self.buttons, self.colors, self.functions):
            btn.setStyleSheet(color)
            self.layout.addWidget(btn)
            btn.clicked.connect(func)

        self.setLayout(self.layout)

        # İşletim sistemi kontrolü
        self.is_windows = sys.platform.startswith('win')

    
    def run_script(self, script_path, baslik):
        cevap = QMessageBox.question(self, 'Onay', 'İşlemi başlatmak istediğinize emin misiniz?', QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.No:
            QMessageBox.information(self, 'İptal', 'İşlem iptal edildi.')
            return
        self.original_dir = os.getcwd()
        os.chdir("..")
        progress = CustomProgressDialog(baslik, self)
        # Thread'i başlat
        self.thread = CMDScriptRunnerThread(script_path)
        self.thread.finished.connect(progress.close)
        self.thread.error.connect(progress.close)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.info.connect(self.info)
        self.thread.start()
        progress.show()

    def on_finished(self, output):
        QMessageBox.information(self, 'Başarılı', output)
        os.chdir(self.original_dir)

    def on_error(self, errors):
        QMessageBox.critical(self, 'Hata', errors)
        os.chdir(self.original_dir)
    def info(self, message):
        None

    def update_google_form(self):
        self.run_script(GOOGLE_FORM_GUNCELLE_BAT if self.is_windows else GOOGLE_FORM_GUNCELLE_SH, baslik = "Google Form Güncelleniyor...")

    def update_readme(self):
        self.run_script(README_GUNCELLE_BAT if self.is_windows else README_GUNCELLE_SH, baslik = "README.md Güncelleniyor...")

    def push_changes(self):
        commit_mesaji, ok_pressed = QInputDialog.getText(self, "Commit Mesajı", "Lütfen commit mesajını giriniz:", QLineEdit.Normal, "")
        if not ok_pressed:
            QMessageBox.information(self, 'İptal', 'İşlem iptal edildi.')
            return
        if not commit_mesaji:
            QMessageBox.critical(self, 'Hata', 'Lütfen commit mesajını giriniz.')
            return
        bat_dosyasi = DEGISIKLIKLERI_GITHUBA_YOLLA_BAT if self.is_windows else DEGISIKLIKLERI_GITHUBA_YOLLA_SH
        bat_scripti = bat_dosyasi + " " + DOKUMANLAR_REPO_YOLU + " \"" + commit_mesaji + "\""
        self.run_script(bat_scripti, baslik = "Değişiklikler Github'a Pushlanıyor...")

    def update_interface(self):
        # Git status kontrolü
        stream = os.popen('git status')
        output = stream.read()

        # Değişiklik olup olmadığını kontrol et
        if "nothing to commit, working tree clean" not in output:
            QMessageBox.critical(None, "Hata", "Dizinde değişiklikler var. Lütfen önce bu değişiklikleri commit yapın veya geri alın.")
            return
        self.run_script(ARAYUZU_GITHULA_ESITLE_BAT if self.is_windows else ARAYUZU_GITHULA_ESITLE_SH, baslik="Arayüz Kodları Güncelleniyor...")

    def start_routine_check(self):
        self.run_script(RUTIN_KONTROL_BAT if self.is_windows else RUTIN_KONTROL_SH, baslik="Rutin Kontrol Yapılıyor...")
