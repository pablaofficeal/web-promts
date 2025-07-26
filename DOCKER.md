# 🐳 Docker инструкции

## Быстрый старт

### 1. Сборка и запуск
```bash
# Собрать и запустить приложение
docker-compose up --build

# Запустить в фоновом режиме
docker-compose up -d --build
```

### 2. Остановка
```bash
# Остановить приложение
docker-compose down

# Остановить и удалить volumes
docker-compose down -v
```

### 3. Просмотр логов
```bash
# Просмотр логов в реальном времени
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f web-prompts
```

## Команды Docker

### Сборка образа
```bash
docker build -t web-prompts .
```

### Запуск контейнера
```bash
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance -v $(pwd)/config:/app/config:ro web-prompts
```

### Вход в контейнер
```bash
docker exec -it web-prompts-app bash
```

## Структура Docker

### Dockerfile
- Использует Python 3.11 slim образ
- Устанавливает системные зависимости
- Создает пользователя для безопасности
- Настраивает переменные окружения

### docker-compose.yml
- Определяет сервис `web-prompts`
- Монтирует volumes для данных и конфигурации
- Настраивает healthcheck
- Создает сеть для контейнеров

### Volumes
- `./instance:/app/instance` - база данных SQLite
- `./config:/app/config:ro` - конфигурационные файлы (только чтение)

## Переменные окружения

| Переменная | Значение | Описание |
|------------|----------|----------|
| `FLASK_APP` | `app.py` | Главный файл приложения |
| `FLASK_ENV` | `production` | Режим работы |
| `PYTHONUNBUFFERED` | `1` | Небуферизованный вывод Python |

## Проблемы и решения

### Проблема: Порт уже занят
```bash
# Изменить порт в docker-compose.yml
ports:
  - "8080:5000"  # Внешний порт 8080
```

### Проблема: Нет доступа к файлам
```bash
# Проверить права доступа
chmod -R 755 ./instance
chmod -R 755 ./config
```

### Проблема: База данных не сохраняется
```bash
# Проверить монтирование volume
docker-compose exec web-prompts ls -la /app/instance
```

## Production рекомендации

1. **Используйте внешнюю базу данных** (PostgreSQL/MySQL)
2. **Настройте reverse proxy** (Nginx)
3. **Добавьте SSL/TLS** сертификаты
4. **Настройте мониторинг** (Prometheus/Grafana)
5. **Используйте secrets** для чувствительных данных

## Пример production docker-compose.yml

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web-prompts

  web-prompts:
    build: .
    expose:
      - "5000"
    volumes:
      - ./instance:/app/instance
      - ./config:/app/config:ro
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
``` 