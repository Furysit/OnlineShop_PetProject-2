// src/pages/Home.jsx
import OrderHistorySlider from "../components/OrderHistory/OrderHistory";
import "./Home.css";

export default function Home() {
  return (
    <>
      <div className="home-container">
      <h1>Добро пожаловать в наш интернет-магазин!</h1>
      <p>
        Этот проект — современное веб-приложение для продажи товаров, реализованное с использованием <strong>FastAPI</strong> на бэкенде и <strong>React</strong> на фронтенде.
      </p>
      <ul>
        <li>🔧 Бэкенд написан на <strong>Python + FastAPI</strong> — современном, асинхронном веб-фреймворке, обеспечивающем высокую производительность.</li>
        <li>🗂️ Взаимодействие с базой данных реализовано через <strong>SQLAlchemy + AsyncSession</strong> (асинхронный доступ).</li>
        <li>🔐 Авторизация JWT с поддержкой ролей (админ/пользователь).</li>
        <li>🛒 Реализована корзина покупок и управление товарами (добавление, удаление, редактирование).</li>
        <li>🖼️ Поддержка загрузки изображений для каждого товара.</li>
        <li>⚙️ Frontend на <strong>React</strong> с использованием хуков и fetch-запросов для работы с API.</li>
      </ul>
      <p>
        Администраторы могут управлять товарами через отдельную панель. Пользователи — просматривать, добавлять товары в корзину и оформлять покупки.
      </p>
    </div>
      <OrderHistorySlider />
    </>
    

  );
}
