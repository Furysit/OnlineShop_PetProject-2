import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ForgotPassword() {
  const [user_email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");

  try {
    const encodedEmail = encodeURIComponent(user_email);
    const url = `http://localhost:8000/api/v1/users/users/forgot_password?user_email=${encodedEmail}`;

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "accept": "*/*"
      },
      body: JSON.stringify({})  // Пустое тело, если сервер требует
    });

    if (response.status === 204) {
      setSent(true);
      setTimeout(() => navigate("/login"), 3000);
    } else {
      throw new Error("Ошибка сервера");
    }
  } catch (err) {
    setError(err.message);
  }
};

  return (
    <div className="auth-container">
      <h2>Восстановление пароля</h2>

      {sent ? (
        <p>Если почта указана верно, вы получите инструкцию на email.</p>
      ) : (
        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="email"
            placeholder="Введите ваш email"
            value={user_email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button type="submit">Отправить</button>
        </form>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
}
