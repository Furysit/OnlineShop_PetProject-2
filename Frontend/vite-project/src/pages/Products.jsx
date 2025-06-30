import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "./Products.css";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState("");
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({
    category_id: "",
    min_price: "",
    max_price: "",
  });

  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, [filters]);

  const fetchProducts = () => {
    const params = new URLSearchParams();
    if (filters.category_id) params.append("category_id", filters.category_id);
    if (filters.min_price) params.append("min_price", filters.min_price);
    if (filters.max_price) params.append("max_price", filters.max_price);

    fetch(`http://localhost:8000/api/v1/products/?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch(() => setMessage("Ошибка загрузки товаров"));
  };

  const fetchCategories = () => {
    fetch("http://localhost:8000/api/v1/products/categories")
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch(() => console.warn("Ошибка загрузки категорий"));
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const addToCart = (productId) => {
    if (!token) {
      toast.warning("Пожалуйста, войдите в аккаунт для добавления в корзину");
      navigate("/login");
      return;
    }

    fetch("http://localhost:8000/api/v1/cart/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ product_id: productId, quantity: 1 }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка при добавлении в корзину");
        return res.json();
      })
      .then(() => toast.success("Товар добавлен в корзину"))
      .catch((err) => setMessage(err.message));
  };

  return (
    <div className="products-container">
      <h1>Все товары</h1>

      {/* 🔽 Фильтры */}
      <div className="filter-bar">
        <select name="category_id" value={filters.category_id} onChange={handleFilterChange}>
          <option value="">Все категории</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>

        <input
          type="number"
          name="min_price"
          value={filters.min_price}
          onChange={handleFilterChange}
          placeholder="Мин. цена"
        />

        <input
          type="number"
          name="max_price"
          value={filters.max_price}
          onChange={handleFilterChange}
          placeholder="Макс. цена"
        />
      </div>

      {message && <div className="products-message">{message}</div>}

      <div className="products-list">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            {product.image_url && (
              <img
                src={`http://localhost:8000${product.image_url}`}
                alt={product.name}
                className="product-img"
              />
            )}
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <strong>{product.price} ₽</strong>
            <button className="add-to-cart-btn" onClick={() => addToCart(product.id)}>
              Добавить в корзину
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
