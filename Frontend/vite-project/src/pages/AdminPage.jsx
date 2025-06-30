import { useEffect, useState } from "react";
import "./AdminPage.css";

export default function AdminPage() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({
    name: "",
    price: "",
    description: "",
    image: null,
  });
  const [editingProduct, setEditingProduct] = useState(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = () => {
    fetch("http://localhost:8000/api/v1/products/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Ошибка при загрузке товаров", err));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (editingProduct) {
      setEditingProduct({ ...editingProduct, [name]: value });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (editingProduct) {
      setEditingProduct({ ...editingProduct, image: file });
    } else {
      setForm({ ...form, image: file });
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("name", form.name);
    formData.append("price", form.price);
    formData.append("description", form.description);
    formData.append("image", form.image);

    try {
      const res = await fetch("http://localhost:8000/api/v1/products/", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      if (!res.ok) throw new Error("Ошибка создания товара");

      const newProduct = await res.json();
      setProducts([...products, newProduct]);
      resetForm();
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("name", editingProduct.name);
    formData.append("price", editingProduct.price);
    formData.append("description", editingProduct.description);
    if (editingProduct.image instanceof File) {
      formData.append("image", editingProduct.image);
    }

    try {
      const res = await fetch(
        `http://localhost:8000/api/v1/products/${editingProduct.id}/`,
        {
          method: "PUT",
          headers: { Authorization: `Bearer ${token}` },
          body: formData,
        }
      );

      if (!res.ok) throw new Error("Ошибка обновления товара");

      const updated = await res.json();
      setProducts(
        products.map((p) => (p.id === updated.id ? updated : p))
      );
      setEditingProduct(null);
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Удалить товар?")) return;

    try {
      await fetch(`http://localhost:8000/api/v1/products/${id}/`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      setProducts(products.filter((p) => p.id !== id));
    } catch (err) {
      console.error("Ошибка удаления", err);
    }
  };

  const resetForm = () => {
    setForm({ name: "", price: "", description: "", image: null });
  };

  return (
    <div className="admin-container">
      <h2>Панель администратора</h2>

      <form
        className="admin-form"
        onSubmit={editingProduct ? handleUpdate : handleCreate}
        encType="multipart/form-data"
      >
        <input
          type="text"
          name="name"
          placeholder="Название"
          value={editingProduct ? editingProduct.name : form.name}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="price"
          placeholder="Цена"
          value={editingProduct ? editingProduct.price : form.price}
          onChange={handleChange}
          required
        />
        <textarea
          name="description"
          placeholder="Описание"
          value={editingProduct ? editingProduct.description : form.description}
          onChange={handleChange}
          required
        />
        <input
          type="file"
          name="image"
          accept="image/*"
          onChange={handleFileChange}
        />

        <button type="submit">
          {editingProduct ? "Сохранить изменения" : "Добавить"}
        </button>
        {editingProduct && (
          <button type="button" onClick={() => setEditingProduct(null)}>
            Отмена
          </button>
        )}
      </form>

      <div className="admin-products">
        {products.map((product) => (
          <div key={product.id} className="admin-product-card">
            {product.image_url && (
              <img
                src={`http://localhost:8000${product.image_url}`}
                alt={product.name}
                className="admin-img"
              />
            )}
            <h3>{product.name}</h3>
            <p>Цена: {product.price}₽</p>
            <p>{product.description}</p>
            <div className="admin-actions">
              <button onClick={() => setEditingProduct(product)}>
                Редактировать
              </button>
              <button onClick={() => handleDelete(product.id)}>Удалить</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
