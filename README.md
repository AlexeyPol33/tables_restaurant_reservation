# Restaurant Table Reservation API 🍽️

![Python](https://img.shields.io/badge/python-3.12.9-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.1-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.2-blue)
![Docker](https://img.shields.io/badge/Docker-24.0.5-blue)

REST API сервис для управления бронированием столиков в ресторане. Позволяет клиентам бронировать столики, а администраторам - управлять расписанием и доступностью мест.

## 🔧 Технологический стек

### Основные технологии
- **Язык программирования**: Python 3.12.9
- **Фреймворк**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Миграции**: Alembic
- **База данных**: PostgreSQL 16

### Дополнительные зависимости
- Pydantic (валидация данных)
- Uvicorn (ASGI сервер)
- Docker (контейнеризация)

## 🚀 Быстрый старт

### Предварительные требования
- Установленный Docker и Docker Compose
- Python 3.12 (если запуск без Docker)

### Запуск с помощью Docker (рекомендуемый способ)
```bash
docker-compose up --build