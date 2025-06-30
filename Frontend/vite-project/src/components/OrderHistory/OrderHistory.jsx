import { useEffect, useState } from "react";
import Slider from "react-slick";

import "./OrderHistory.css"


export default function OrderHistorySlider() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {

    if (!token) {
      setLoading(false); // Не делаем fetch, просто скрываем компонент
      return;
    }
    
    fetch("http://localhost:8000/api/v1/orders/my_orders", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
        })
      .then(async (res) => {
        if (!res.ok) throw new Error("Ошибка загрузки истории заказов");
        const data = await res.json();
        setOrders(data);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const settings = {
    dots: true,
    infinite: orders.length > 3,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 768,
        settings: { slidesToShow: 1 },
      },
    ],
  };

  if (loading) return <p>Загрузка истории заказов...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (orders.length === 0) return <p>Здесь будет ваша история заказов.</p>;

  return (
    <div style={{ margin: "20px" }}>
      <h2>История ваших заказов</h2>
      <Slider {...settings}>
        {orders.map((order) => (
            <div key={order.id} style={{ padding: "10px" }}>
                <div
                style={{
                    border: "1px solid #ccc",
                    borderRadius: "8px",
                    padding: "15px",
                    minHeight: "150px",
                    background: "#fafafa",
                }}
                >
                <h3>Заказ #{order.id}</h3>
                <p>Дата: {new Date(order.created_at).toLocaleDateString()}</p>
                <p>Сумма: {order.total_price}₽</p>
                <p>Товары:</p>
                <ul style={{ maxHeight: "70px", overflowY: "auto" }}>
                  {(order.order_items ?? []).map((item) => (
                    <li key={item.id}>
                      {item.product ? `${item.product.name} — ${item.quantity} шт.` : "Товар удалён"}
                    </li>
                  ))}
                </ul>
                </div>
            </div>
            ))}
      </Slider>
    </div>
  );
}
