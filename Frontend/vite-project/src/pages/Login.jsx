import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
      const response = await fetch("http://localhost:8000/api/v1/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString(),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Ошибка входа");
      }

      localStorage.setItem("token", data.access_token);
      if (data.user) {
        localStorage.setItem("user", JSON.stringify(data.user));
      }
      navigate("/"); // Перенаправление после входа
      window.location.reload();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Вход</h2>
      <form onSubmit={handleLogin} className="login-form">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Войти</button>
      </form>
      
      {error && <p className="error">{error}</p>}
      <div className="login-links">
      <p>
        <a href="/ForgotPassword">Забыли пароль?</a>
      </p>
      <p>
        Нет аккаунта? <a href="/Register">Зарегистрироваться</a>
      </p>
    </div>
    </div>
  );
}
