@echo off
chcp 65001 > nul
echo ===================================================
echo     AGROSTAR DAVOMAT - ANDROID APK YIG'ISH         
echo ===================================================
echo.

where flutter >nul 2>nul
if %errorlevel% neq 0 (
    echo [XATOLIK] Kompyuterda Flutter SDK topilmadi!
    echo.
    echo APK yaratishning 2 ta oson yo'li mavjud:
    echo 1. GITHUB ACTIONS (Tavsiya etiladi, hech narsa o'rnatish shart emas):
    echo    Ushbu papkadagi kodni GitHub repozitoriyingizga push qiling.
    echo    .github/workflows/build_apk.yml avtomatik tarzda bulutda APK yig'ib beradi.
    echo.
    echo 2. LOKAL KOMPYUTERDA:
    echo    Flutter SDK (https://docs.flutter.dev/get-started/install/windows)
    echo    va Android Studio o'rnatilgach, ushbu buyruqni qayta ishga tushiring.
    echo.
    pause
    exit /b 1
)

cd mobile_app
echo [1/3] Paketlar yuklanmoqda (flutter pub get)...
call flutter pub get

echo.
echo [2/3] Android Release APK yig'ilmoqda (flutter build apk --release)...
call flutter build apk --release

echo.
echo [3/3] Natija:
if exist "build\app\outputs\flutter-apk\app-release.apk" (
    echo.
    echo ============================================================
    echo [MUVAFFAQIYATLI] APK tayyor!
    echo Fayl yo'li: mobile_app\build\app\outputs\flutter-apk\app-release.apk
    echo ============================================================
    explorer /select,build\app\outputs\flutter-apk\app-release.apk
) else (
    echo [XATOLIK] APK yig'ishda xatolik yuz berdi. Yuqoridagi loglarni tekshiring.
)

pause
