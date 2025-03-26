import { Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import AdminDashboard from "./pages/AdminDashboard";
import CustomerDashboard from "./pages/CustomerDashboard";
import Profile from "./pages/Profile";
import Transactions from "./pages/Transactions";
import FinanceDetails from "./pages/FinanceDetails";
import Navbar from "./components/Navbar";
import AddReview from "./pages/AddReview";
import MyReviews from "./pages/MyReviews";
import Insights from "./pages/Insights";

const App = () => {
  const { user } = useContext(AuthContext);

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/admin-dashboard"
          element={user?.role === "admin" ? <AdminDashboard /> : <Navigate to="/" />}
        />
        <Route
          path="/insights"
          element={user?.role === "admin" ? <Insights /> : <Navigate to="/" />}
        />
        <Route
          path="/customer-dashboard"
          element={user?.role === "customer" ? <CustomerDashboard /> : <Navigate to="/" />}
        />
        <Route path="/add-review" element={<AddReview />} />
        <Route path="/my-reviews" element={<MyReviews />} />
        <Route
          path="/profile"
          element={user?.role === "customer" ? <Profile /> : <Navigate to="/" />}
        />
        <Route
          path="/transactions"
          element={user?.role === "customer" ? <Transactions /> : <Navigate to="/" />}
        />
        <Route
          path="/financedetails"
          element={user?.role === "customer" ? <FinanceDetails /> : <Navigate to="/" />}
        />
      </Routes>
    </>
  );
};

export default App;
