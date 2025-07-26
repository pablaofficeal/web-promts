@echo off
echo 🚀 Запуск генератора промптов...
echo.

echo Выберите способ запуска:
echo 1. Локальный запуск (Python)
echo 2. Docker запуск
echo 3. Выход
echo.

set /p choice="Введите номер (1-3): "

if "%choice%"=="1" goto local
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto exit
goto invalid

:local
echo.
echo 📦 Установка зависимостей...
pip install -r requirements.txt
echo.
echo 🏃 Запуск приложения...
python app.py
goto end

:docker
echo.
echo 🐳 Запуск через Docker...
docker-compose up --build
goto end

:invalid
echo.
echo ❌ Неверный выбор. Попробуйте снова.
pause
goto start

:exit
echo.
echo 👋 До свидания!
pause
exit

:end
pause 