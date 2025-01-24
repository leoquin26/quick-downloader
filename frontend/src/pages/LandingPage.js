import React from "react";
import {
  Box,
  Button,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
} from "@mui/material";
import Header from "../components/Header";
import Features from "../components/Features";
import Footer from "../components/Footer";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
  const navigate = useNavigate();

  const platforms = [
    {
      name: "YouTube",
      description: "Download videos and audio from YouTube in various formats.",
      path: "/youtube",
      color: "#FF0000",
      textColor: "#FFFFFF",
    },
    {
      name: "TikTok",
      description: "Download TikTok videos without watermark easily.",
      path: "/tiktok",
      color: "#000000",
      textColor: "#FFFFFF",
    },
    {
      name: "Instagram",
      description: "Download Instagram videos without watermark easily.",
      path: "/instagram",
      color: "transparent",
      textColor: "#FFFFFF",
      gradient:
        "linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)",
    },
    {
      name: "SoundCloud",
      description: "Download tracks from SoundCloud with high-quality audio.",
      path: "/soundcloud",
      color: "#FF8800",
      textColor: "#FFFFFF",
    },
  ];

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div>
      <Header />
      <Box
        sx={{
          textAlign: "center",
          padding: "100px 20px",
          backgroundColor: "primary.main",
          color: "white",
        }}
      >
        <Container>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: "bold" }}>
            Download Videos & Audio Seamlessly
          </Typography>
          <Typography variant="h6" gutterBottom>
            Easily download videos and audio from YouTube, TikTok, Instagram, and SoundCloud in any format and quality.
          </Typography>
        </Container>
      </Box>

      <Box sx={{ padding: "50px 20px", backgroundColor: "background.paper" }}>
        <Container>
          <Typography
            variant="h4"
            align="center"
            gutterBottom
            sx={{ fontWeight: "bold", marginBottom: "30px" }}
          >
            Select a Platform
          </Typography>
          <Grid container spacing={4} justifyContent="center">
            {platforms.map((platform) => (
              <Grid item xs={12} sm={6} md={4} key={platform.name}>
                <Card
                  sx={{
                    textAlign: "center",
                    boxShadow: 3,
                    padding: "20px",
                    borderRadius: "8px",
                    transition: "transform 0.3s, box-shadow 0.3s",
                    "&:hover": {
                      transform: "scale(1.05)",
                      boxShadow: 6,
                    },
                  }}
                >
                  <CardContent>
                    <Typography
                      variant="h6"
                      gutterBottom
                      sx={{ fontWeight: "bold" }}
                    >
                      {platform.name}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ marginBottom: "20px" }}
                    >
                      {platform.description}
                    </Typography>
                    <Button
                      variant="contained"
                      sx={{
                        backgroundColor:
                          platform.name === "Instagram" ||
                          platform.name === "SoundCloud"
                            ? platform.color
                            : platform.color,
                        backgroundImage:
                          platform.name === "Instagram"
                            ? platform.gradient
                            : "none",
                        color: platform.textColor,
                        textTransform: "uppercase",
                        fontWeight: "bold",
                        "&:hover": {
                          opacity: 0.8,
                        },
                        border:
                          platform.name === "Instagram" ||
                          platform.name === "SoundCloud"
                            ? "none"
                            : `1px solid ${platform.color}`,
                      }}
                      onClick={() => handleNavigate(platform.path)}
                    >
                      Go to {platform.name}
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      <Features />
      <Footer />
    </div>
  );
};

export default LandingPage;
