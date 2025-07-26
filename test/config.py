import json
import os

def test_config_files():
    print("🧪 Тестирование конфигурационных файлов...")
    
    config_dir = 'config'
    
    # Проверяем наличие всех файлов
    required_files = [
        'technologies.json',
        'frameworks.json', 
        'prompt_rules.json',
        'prompts.json'
    ]
    
    print(f"\n1. Проверка файлов в папке {config_dir}:")
    for filename in required_files:
        filepath = os.path.join(config_dir, filename)
        if os.path.exists(filepath):
            print(f"   ✅ {filename}")
        else:
            print(f"   ❌ {filename} - НЕ НАЙДЕН!")
    
    # Проверяем структуру prompts.json
    print(f"\n2. Проверка структуры prompts.json:")
    try:
        with open(os.path.join(config_dir, 'prompts.json'), 'r', encoding='utf-8') as f:
            prompts = json.load(f)
        
        print(f"   ✅ Файл загружен успешно")
        print(f"   📊 Количество технологий: {len(prompts)}")
        
        for tech, tech_prompts in prompts.items():
            print(f"      {tech}: {len(tech_prompts)} промптов")
            
    except Exception as e:
        print(f"   ❌ Ошибка загрузки: {e}")
    
    # Проверяем соответствие ID
    print(f"\n3. Проверка соответствия ID:")
    try:
        with open(os.path.join(config_dir, 'technologies.json'), 'r', encoding='utf-8') as f:
            techs = json.load(f)
        
        with open(os.path.join(config_dir, 'frameworks.json'), 'r', encoding='utf-8') as f:
            frameworks = json.load(f)
        
        with open(os.path.join(config_dir, 'prompts.json'), 'r', encoding='utf-8') as f:
            prompts = json.load(f)
        
        # Проверяем, что все технологии из prompts.json есть в technologies.json
        for tech_id in prompts.keys():
            tech_exists = any(t['id'] == tech_id for t in techs)
            if tech_exists:
                print(f"   ✅ Технология '{tech_id}' найдена")
            else:
                print(f"   ❌ Технология '{tech_id}' НЕ найдена в technologies.json")
        
        # Проверяем фреймворки
        for tech_id, tech_prompts in prompts.items():
            for fw_id in tech_prompts.keys():
                fw_exists = any(f['id'] == fw_id for f in frameworks.get(tech_id, []))
                if fw_exists:
                    print(f"   ✅ Фреймворк '{fw_id}' для '{tech_id}' найден")
                else:
                    print(f"   ❌ Фреймворк '{fw_id}' для '{tech_id}' НЕ найден в frameworks.json")
                    
    except Exception as e:
        print(f"   ❌ Ошибка проверки: {e}")

if __name__ == '__main__':
    test_config_files() 