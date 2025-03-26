import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Container, TextField, Button, Typography, Box } from "@mui/material";
import { useLocation } from "react-router-dom";

const Login = () => {
  const { login } = useContext(AuthContext);
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const defaultRole = params.get("role") || "customer";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role] = useState(defaultRole);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(username, password, role);
  };

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 5, p: 3, borderRadius: 2, boxShadow: 3, textAlign: "center", backgroundColor: "white" }}>
        <Typography variant="h5" sx={{ fontWeight: "bold", color: "#b31b1b", mb: 2 }}>
          Login as {role.charAt(0).toUpperCase() + role.slice(1)}
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField fullWidth label="Username" variant="outlined" margin="normal" value={username} onChange={(e) => setUsername(e.target.value)} required />
          <TextField fullWidth label="Password" type="password" variant="outlined" margin="normal" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Button fullWidth type="submit" variant="contained" sx={{ mt: 2, backgroundColor: "#b31b1b", color: "white" }}>
            Login
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default Login;
