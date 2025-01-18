
# Проект с микросервисами: Bet Maker и Line Provider

Этот репозиторий содержит два микросервиса, работающих вместе:
1. **Bet Maker**: предоставляет API для управления ставками пользователей.
2. **Line Provider**: предоставляет данные о событиях для ставок.

## Установка и запуск

### Системные требования
- Docker версии 20.10 или выше
- Docker Compose версии 1.29 или выше

### Шаги для запуска

1. Клонируйте репозиторий:
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-folder
   ```

2. Создайте `.env` файл в корне репозитория с содержимым:
   ```env
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   DB_HOST=db
   DB_PORT=5432
   REDIS_URL=redis://redis:6379/0
   ```

3. Запустите оба сервиса:
   ```bash
   docker-compose up --build
   ```

4. Оба сервиса будут доступны:
   - **Bet Maker**: http://localhost:8001
   - **Line Provider**: http://localhost:8000

## API

### Bet Maker
- **`GET /bets`**: Получение всех ставок.
- **`POST /bet`**: Создание новой ставки.
  ```json
  {
    "event_id": "string",
    "amount": 100
  }
  ```
- **`GET /events`**: Получение всех доступных событий для ставок.

- **Документация Swagger для Bet Maker**: [http://127.0.0.1:8001/docs#/](http://127.0.0.1:8001/docs#/)

### Line Provider
- **`GET /events`**: Получение всех событий для ставок.
- **`POST /events`**: Создание нового события.
  ```json
  {
    "odds": 2.5,
    "deadline": "2025-01-15T20:00:00+00:00"
  }
  ```
- **Документация Swagger для Line Provider**: [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)

## Тесты

Тесты находятся в директории `line-provider/app/tests/` и покрывают функционал микросервиса Line Provider.
