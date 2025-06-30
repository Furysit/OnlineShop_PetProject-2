import { Link, NavLink, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "./Header.css";

export default function Header() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
    window.location.reload();
  };

  return (
    <header className="header">
      <nav className="nav">
        <Link to="/" className="nav-link">Главная</Link>
        <Link to="/products" className="nav-link">Товары</Link>
        <Link to="/cart" className="nav-link">Корзина</Link>
        {user?.role === "admin" && (
          <NavLink to="/admin" className="nav-link">Админка</NavLink>
        )}
      </nav>
      <div>
        {token ? (
          <button onClick={logout} className="logout-button">Выйти</button>
        ) : (
          <Link to="/login" className="nav-link">Вход</Link>
        )}
      </div>
    </header>
  );
}
