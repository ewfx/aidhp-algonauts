import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Container, TextField, Button, Typography, Select, MenuItem, FormControl, InputLabel, Box } from "@mui/material";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("customer");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/auth/signup", { username, password, role });
      alert("Signup successful! Please login.");
      navigate("/login");
    } catch (error) {
      alert("Signup failed. Try again.");
    }
  };

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 5, p: 3, borderRadius: 2, boxShadow: 3, textAlign: "center", backgroundColor: "white" }}>
        <Typography variant="h5" sx={{ fontWeight: "bold", color: "#b31b1b", mb: 2 }}>
          Signup
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            variant="outlined"
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            variant="outlined"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Role</InputLabel>
            <Select value={role} onChange={(e) => setRole(e.target.value)} label="Role">
              <MenuItem value="customer">Customer</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
            </Select>
          </FormControl>
          <Button
            fullWidth
            type="submit"
            variant="contained"
            sx={{ backgroundColor: "#b31b1b", color: "white", mt: 2, "&:hover": { backgroundColor: "#930000" } }}
          >
            Signup
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default Signup;
