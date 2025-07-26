#!/bin/bash

echo "🚀 Запуск генератора промптов..."
echo

echo "Выберите способ запуска:"
echo "1. Локальный запуск (Python)"
echo "2. Docker запуск"
echo "3. Выход"
echo

read -p "Введите номер (1-3): " choice

case $choice in
    1)
        echo
        echo "📦 Установка зависимостей..."
        pip install -r requirements.txt
        echo
        echo "🏃 Запуск приложения..."
        python app.py
        ;;
    2)
        echo
        echo "🐳 Запуск через Docker..."
        docker-compose up --build
        ;;
    3)
        echo
        echo "👋 До свидания!"
        exit 0
        ;;
    *)
        echo
        echo "❌ Неверный выбор. Попробуйте снова."
        exit 1
        ;;
esac 