import { useState } from "react";

export default function AddProductForm() {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    price: "",
    image: null,
  });

  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === "image") {
      setFormData({ ...formData, image: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.image) {
      setMessage("Пожалуйста, выберите изображение");
      return;
    }

    const data = new FormData();
    data.append("name", formData.name);
    data.append("description", formData.description);
    data.append("price", formData.price);
    data.append("image", formData.image);

    try {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:8000/api/v1/products/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: data,
      });

      if (!res.ok) throw new Error("Ошибка при создании товара");

      setSuccess(true);
      setMessage("Товар успешно добавлен!");
      setFormData({ name: "", description: "", price: "", image: null });

      setTimeout(() => {
        setMessage("");
        setSuccess(false);
      }, 3000);
    } catch (err) {
      setSuccess(false);
      setMessage(err.message);
    }
  };

  return (
    <div className="add-product-container">
      <h2>Добавить товар</h2>
      <form onSubmit={handleSubmit} className="add-product-form">
        <input
          type="text"
          name="name"
          placeholder="Название"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <textarea
          name="description"
          placeholder="Описание"
          value={formData.description}
          onChange={handleChange}
          required
        ></textarea>
        <input
          type="number"
          name="price"
          placeholder="Цена"
          value={formData.price}
          onChange={handleChange}
          required
        />
        <input type="file" name="image" accept="image/*" onChange={handleChange} />
        <button type="submit">Создать товар</button>
      </form>
      {message && (
        <div className={`form-message ${success ? "success" : "error"}`}>
          {message}
        </div>
      )}
    </div>
  );
}
    