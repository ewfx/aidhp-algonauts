import { AppBar, Toolbar, Typography } from "@mui/material";
import { useLocation } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();
  const isHomePage = location.pathname === "/";

  return (
    <AppBar position="static" sx={{ backgroundColor: "#b31b1b" }}>
      <Toolbar>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
          FinSight
        </Typography>
        {!isHomePage && (
          <>
            {/* Add buttons here if needed for other pages */}
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
