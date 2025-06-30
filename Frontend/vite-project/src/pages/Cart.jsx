import { useEffect, useState, useMemo  } from "react";
import { useNavigate } from "react-router-dom"; 
import { toast } from "react-toastify";

import "./Cart.css";

export default function Cart() {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const totalPrice = useMemo(() => {
  return cart.reduce((acc, item) => acc + item.quantity * item.product.price, 0);
}, [cart]);

  useEffect(() => {

    if (!token) {
      navigate("/login"); 
      return;
    }

    fetch("http://localhost:8000/api/v1/cart/get_cart_detailed", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Ошибка загрузки корзины");
        const data = await res.json();
        setCart(data);
      })
      .catch((err) => setMessage(err.message))
      .finally(() => setLoading(false));
  }, [token,navigate]);

  const handleOrder = () => {
    fetch("http://localhost:8000/api/v1/orders/create_order", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Ошибка при оформлении заказа");
        const data = await res.json();
        toast.success(`Заказ #${data.id} создан на сумму ${data.total_price}₽`);
        setCart([]);
      })
      .catch((err) => setMessage(err.message));
  };

  const handleRemove = async (productId) => {
  try {
      const res = await fetch(
        `http://localhost:8000/api/v1/cart/remove_from_cart?product_id=${productId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (!res.ok) throw new Error("Не удалось удалить товар");
      setCart((prev) => prev.filter((item) => item.product.id !== productId));
    } catch (err) {
      setMessage(err.message);
    }
  };

  const handleQuantityChange = async (productId, newQuantity) => {
  try {
    if (newQuantity < 1) return; // не даём уменьшить до 0

    const res = await fetch(
      `http://localhost:8000/api/v1/cart/change_quantity?product_id=${productId}&quantity=${newQuantity}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (!res.ok) throw new Error("Ошибка изменения количества");

    setCart((prev) =>
      prev.map((item) =>
        item.product.id === productId
          ? { ...item, quantity: newQuantity }
          : item
      )
    );
  } catch (err) {
    setMessage(err.message);
  }
};


  if (loading) return <p className="cart-loading">Загрузка корзины...</p>;

  return (
    <div className="cart-container">
      <h1>Корзина</h1>
      {cart.length === 0 ? (
        <p className="cart-empty">Корзина пуста</p>
      ) : (
        <>
          <div className="cart-items">
            {cart.map((item) => (
              <div key={item.id} className="cart-item">
                <strong>{item.product.name}</strong> — {item.quantity} шт.
                <br />
                Цена: {item.product.price}₽
                <div className="quantity-controls">
                  <button onClick={() => handleQuantityChange(item.product.id, item.quantity - 1)}>-</button>
                  <span style={{ margin: "0 10px" }}>{item.quantity}</span>
                  <button onClick={() => handleQuantityChange(item.product.id, item.quantity + 1)}>+</button>

                  <button
                    onClick={() => handleRemove(item.product.id)}
                    style={{
                      marginLeft: "20px",
                      background: "red",
                      color: "white",
                      border: "none",
                      padding: "4px 8px",
                      borderRadius: "4px",
                    }}
                  >
                    Удалить
                  </button>
                </div>
              </div>
            ))}
          </div>
            <div className="cart-total">
              <strong>Итоговая сумма:</strong> {totalPrice}₽
            </div>
          <button onClick={handleOrder} className="cart-order-btn">
            Оформить заказ
          </button>
        </>
      )}
      {message && <div className="cart-message">{message}</div>}
      
    </div>
  );
}
