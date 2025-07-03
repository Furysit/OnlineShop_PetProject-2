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
   - DB_URL=postgresql+asyncpg://user:password@localhost/dbname
   - SECRET_KEY=your-secret-key
   - ALGORITHM=HS256
4. Запустить сервер:
   - cd backend
   - poetry run start
   - Сервер будет доступен по адресу: http://localhost:8000

Документация API (Swagger/Redoc): http://localhost:8000/docs


### Запуск фронта:
   
   - cd frontend
   - cd vite-project
   - npm install
   - npm run dev

### БД подключать в .env(DB_URL) POSTGRESQL
    
### 🌐 API Endpoints (основные)
1. POST /auth/register - регистрация
2. POST /auth/login - авторизация
3. GET /products - список товаров
4. POST /orders - создание заказа
5. GET /orders/history - история заказов
![image](https://github.com/user-attachments/assets/841419e1-37a5-48fc-b85d-ee38d11b2f6d)
![image](https://github.com/user-attachments/assets/b8679af8-fcda-4ed7-b417-73c1f79fec3c)



(Полный список endpoints смотрите в Swagger)

