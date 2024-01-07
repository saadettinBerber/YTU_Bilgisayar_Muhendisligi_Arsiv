@echo off
cls

:: Python'un yüklü olup olmadığını kontrol edin
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3 bulunamadi. Lutfen https://www.python.org/downloads/ adresinden yukleyin.
    echo Yukleme sirasinda "Add Python to PATH" secenegini isaretlediginizden emin olun.
    pause
    exit /b
)

:: pip'in yüklü olup olmadığını kontrol edin
pip3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip3 bulunamadi, Python'unuz ile birlikte otomatik olarak yuklenmesi gerekirdi.
    echo Yukleme sirasinda bir sorun olmus olabilir. Python'u tekrar yuklemeyi deneyin.
    pause
    exit /b
)

:: Gerekli kütüphaneleri yükleyin
echo Gerekli kutuphaneler kontrol ediliyor ve yukleniyor...

:: gereksinimler.txt dosyasındaki her paketi kontrol et
for /F %%i in (gereksinimler.txt) do (
    pip show %%i >nul 2>&1
    if not %errorlevel%==0 (
        echo %%i yukleniyor...
        pip install %%i
    )
)

:: readme_olusturma_arayuzu klasörüne çıkın ve main.py'yi çalıştırın
cd %~dp0\readme_guncelleme_arayuzu_python
start pythonw main.py

echo İşlem tamamlandı.
