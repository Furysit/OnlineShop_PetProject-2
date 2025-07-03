import { useState } from "react";
import { useNavigate } from "react-router-dom";


export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:8000/api/v1/users/users/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password,
          username: fullName,
        }),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.detail || "Ошибка регистрации");

      navigate("/login");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-container">
      <h2>Регистрация</h2>
      <form onSubmit={handleRegister} className="auth-form">
        <input
          type="text"
          placeholder="Имя"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
        />
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
        <button type="submit">Зарегистрироваться</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
