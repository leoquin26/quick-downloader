import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate("/"); 
  };

  return (
    <AppBar position="static" color="inherit" elevation={1}>
      <Container>
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            sx={{ flexGrow: 1, fontWeight: "bold", cursor: "pointer" }}
            onClick={handleNavigate}
          >
            MyTube Downloader
          </Typography>
          <Button color="primary" href="#features">
            Features
          </Button>
          <Button color="primary" href="#testimonials">
            Testimonials
          </Button>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;
