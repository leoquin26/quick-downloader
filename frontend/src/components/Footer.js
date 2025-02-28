import React from "react";
import { Box, Typography, Link, Container } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";

const Footer = () => {
  return (
    <Box
      sx={{
        textAlign: "center",
        padding: "20px 0",
        backgroundColor: "background.default",
        color: "text.secondary",
        marginTop: "auto",
      }}
      id="contact"
    >
      <Container>
        <Typography variant="body2">
          &copy; 2025 MyTube Downloader. All rights reserved.
        </Typography>
        <Typography variant="body2" sx={{ marginTop: "5px" }}>
          Contact us:{" "}
          <Link href="mailto:support@mytube.com" color="primary">
            support@mytube.com
          </Link>
        </Typography>
        <Typography variant="body2" sx={{ marginTop: "5px" }}>
          <Link component={RouterLink} to="/terms-and-conditions" color="primary">
            Terms and Conditions
          </Link>
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
