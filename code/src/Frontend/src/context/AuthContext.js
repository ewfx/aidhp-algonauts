import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (token && role) {
      setUser({ token, role });
    }
  }, []);

  const login = async (username, password, role) => {
    try {
      const response = await axios.post("http://localhost:5000/auth/login", { username, password ,role},{ withCredentials: true });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);
      localStorage.setItem("role", role);
      setUser({ token: access_token, role });

      navigate(role === "admin" ? "/admin-dashboard" : "/customer-dashboard");
    } catch (error) {
      alert("Invalid credentials");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setUser(null);
    navigate("/");
  };

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>;
};
