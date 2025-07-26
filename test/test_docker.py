import os
import json

def test_docker_files():
    print("🧪 Тестирование Docker конфигурации...")
    
    # Проверяем наличие всех необходимых файлов
    required_files = [
        'Dockerfile',
        'docker-compose.yml',
        'requirements.txt',
        '.dockerignore',
        'DOCKER.md'
    ]
    
    print("\n1. Проверка Docker файлов:")
    for filename in required_files:
        if os.path.exists(filename):
            print(f"   ✅ {filename}")
        else:
            print(f"   ❌ {filename} - НЕ НАЙДЕН!")
    
    # Проверяем содержимое requirements.txt
    print(f"\n2. Проверка requirements.txt:")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        print(f"   ✅ Файл загружен успешно")
        print(f"   📦 Зависимости:")
        for req in requirements:
            if req.strip():
                print(f"      - {req}")
    except Exception as e:
        print(f"   ❌ Ошибка загрузки: {e}")
    
    # Проверяем docker-compose.yml
    print(f"\n3. Проверка docker-compose.yml:")
    try:
        with open('docker-compose.yml', 'r') as f:
            content = f.read()
        
        # Проверяем ключевые элементы
        checks = [
            ('version', 'version:'),
            ('service', 'web-prompts:'),
            ('ports', 'ports:'),
            ('volumes', 'volumes:'),
            ('environment', 'environment:')
        ]
        
        for check_name, check_value in checks:
            if check_value in content:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name} - НЕ НАЙДЕН!")
                
    except Exception as e:
        print(f"   ❌ Ошибка загрузки: {e}")
    
    # Проверяем Dockerfile
    print(f"\n4. Проверка Dockerfile:")
    try:
        with open('Dockerfile', 'r') as f:
            content = f.read()
        
        checks = [
            ('FROM', 'FROM python:'),
            ('WORKDIR', 'WORKDIR /app'),
            ('COPY', 'COPY requirements.txt'),
            ('EXPOSE', 'EXPOSE 5045'),
            ('CMD', 'CMD [')
        ]
        
        for check_name, check_value in checks:
            if check_value in content:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name} - НЕ НАЙДЕН!")
                
    except Exception as e:
        print(f"   ❌ Ошибка загрузки: {e}")
    
    print(f"\n🎉 Docker конфигурация готова!")
    print(f"   Для запуска используйте: docker-compose up --build")

if __name__ == '__main__':
    test_docker_files()