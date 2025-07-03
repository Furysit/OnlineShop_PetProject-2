import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";
import Header from "./components/Header/Header";
import Products from "./pages/Products";
import Home from "./pages/Home";
import Cart from "./pages/Cart";
import Login from "./pages/Login";
import AdminPage from "./pages/AdminPage";
import Register from "./pages/Register";
import ForgotPassword from "./pages/ForgotPassword";


export default function App() {
  

  return (
    <Router>
      <Header />
      <main className="main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/login" element={<Login />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/Register" element={<Register />} />
          <Route path="/ForgotPassword" element={<ForgotPassword />} />

        </Routes>
        <ToastContainer
        position="top-right"
        autoClose={2000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
      />
      </main>
    </Router>
  );
}
