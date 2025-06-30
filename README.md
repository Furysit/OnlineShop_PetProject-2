# 🛍️ Fullstack Магазин на FastAPI + React

Это простой e-commerce проект, реализованный на **FastAPI (бэкенд)** и **React (фронтенд)**. Поддерживает регистрацию, авторизацию, добавление товаров в корзину, оформление заказов и просмотр истории.

---

## 📦 Backend

### Стек:
- FastAPI (асинхронный API)
- SQLAlchemy (Async ORM)
- PostgreSQL (или SQLite)
- Alembic (миграции)
- Poetry (для управления зависимостями)

### Запуск бэкенда:
1. Установить все зависимости (poetry install)
2. Создать .env файл с кофигурацией:
   '''bash
   DB_URL=postgresql+asyncpg://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
4. Запустить сервер:
   -cd backend
   -poetry run start
Сервер будет доступен по адресу: http://localhost:8000

Документация API (Swagger/Redoc): http://localhost:8000/docs


### Запуск фронта:
   '''bash
   -cd frontend
   -cd vite-project
   npm install
   -npm run dev

### БД подключать в .env(DB_URL) POSTGRESQL
    
🌐 API Endpoints (основные)
POST /auth/register - регистрация

POST /auth/login - авторизация

GET /products - список товаров

POST /orders - создание заказа

GET /orders/history - история заказов

(Полный список endpoints смотрите в Swagger)

