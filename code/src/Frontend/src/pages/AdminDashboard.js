import { useNavigate } from "react-router-dom";
import { Button, Container, Typography, Box } from "@mui/material";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

const AdminDashboard = () => {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  return (
    <Container>
      <Box sx={{ mt: 5, textAlign: "center" }}>
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#b31b1b", mb: 2 }}>
          Admin Dashboard
        </Typography>
        <Button onClick={() => navigate("/insights")} variant="contained" sx={{ m: 1 }}>
          Insights
        </Button>
        <Button onClick={logout} variant="contained" color="error" sx={{ m: 1 }}>
          Logout
        </Button>
      </Box>
    </Container>
  );
};

export default AdminDashboard;
