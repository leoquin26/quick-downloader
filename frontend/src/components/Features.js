import React from "react";
import { Box, Container, Grid, Typography, Card, CardContent } from "@mui/material";

const Features = () => {
  const features = [
    { title: "High-Quality Downloads", description: "Download videos and audio in 320kbps, 1080p, and more." },
    { title: "User-Friendly", description: "Simple and intuitive interface for quick downloads." },
    { title: "Secure & Reliable", description: "No malware, just fast and safe downloads." },
  ];

  return (
    <Box
      sx={{
        padding: "50px 20px",
        backgroundColor: "background.default",
      }}
      id="features"
    >
      <Container>
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{
            fontWeight: "bold",
            marginBottom: "40px",
          }}
        >
          Why Choose MyTube Downloader?
        </Typography>
        <Grid container spacing={4} justifyContent="center">
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  height: "100%",
                  boxShadow: 4,
                  borderRadius: 2,
                  transition: "transform 0.2s, box-shadow 0.2s",
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
                    sx={{ fontWeight: "bold", textAlign: "center" }}
                  >
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center" }}>
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Features;
