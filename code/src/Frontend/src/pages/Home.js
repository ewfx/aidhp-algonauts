import { useState } from "react";
import { Container, Button, Typography, Box, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import { Link } from "react-router-dom";

const Home = () => {
  const [role, setRole] = useState("customer");

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 5, p: 3, borderRadius: 2, boxShadow: 3, textAlign: "center", backgroundColor: "white" }}>
        <Typography variant="h5" sx={{ fontWeight: "bold", color: "#b31b1b", mb: 2 }}>
          Welcome to FinSight
        </Typography>

        <FormControl fullWidth margin="normal">
          <InputLabel>Select Role</InputLabel>
          <Select value={role} onChange={(e) => setRole(e.target.value)} label="Role">
            <MenuItem value="customer">Customer</MenuItem>
            <MenuItem value="admin">Admin</MenuItem>
          </Select>
        </FormControl>

        <Button component={Link} to={`/login?role=${role}`} variant="contained" sx={{ mt: 2, mr: 1, backgroundColor: "#b31b1b", color: "white" }}>
          Login
        </Button>
        <Button component={Link} to={`/signup?role=${role}`} variant="contained" sx={{ mt: 2, backgroundColor: "#b31b1b", color: "white" }}>
          Signup
        </Button>
      </Box>
    </Container>
  );
};

export default Home;
