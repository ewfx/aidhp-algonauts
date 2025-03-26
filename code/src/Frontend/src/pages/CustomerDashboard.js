import { useNavigate } from "react-router-dom";
import { Button, Container, Typography, Box } from "@mui/material";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

const CustomerDashboard = () => {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  return (
    <Container>
      <Box sx={{ mt: 5, textAlign: "center" }}>
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#b31b1b", mb: 2 }}>
          Customer Dashboard
        </Typography>
        <Button onClick={() => navigate("/profile")} variant="contained" sx={{ m: 1 }}>
          Profile
        </Button>
        <Button onClick={() => navigate("/transactions")} variant="contained" sx={{ m: 1 }}>
          Transactions
        </Button>
        <Button onClick={() => navigate("/financedetails")} variant="contained" sx={{ m: 1 }}>
          Financial Profile
        </Button>
        <Button onClick={() => navigate("/add-review")} variant="contained" sx={{ m: 1 }}>
          Add Review
        </Button>
        <Button onClick={() => navigate("/my-reviews")} variant="contained" sx={{ m: 1 }}>
          View My Reviews
        </Button>
        <Button onClick={logout} variant="contained" color="error" sx={{ m: 1 }}>
          Logout
        </Button>
      </Box>
    </Container>
  );
};

export default CustomerDashboard;
