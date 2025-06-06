import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import Cookies from "js-cookie"; // Import js-cookie to manage cookies
import RatingComponent from "./RatingComponent"; // Importar componente de calificación
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  CircularProgress,
  Snackbar,
  Alert,
  Card,
  CardMedia,
  CardContent,
  CardActions,
} from "@mui/material";
import axios from "axios";

const InstagramModule = () => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({
    open: false,
    message: "",
    severity: "success",
  });
  const [videoInfo, setVideoInfo] = useState(null);
  const [showRating, setShowRating] = useState(false); // Mostrar calificación después de la descarga
  const [userSession, setUserSession] = useState(null); // State to store user session
  const API_URL = process.env.REACT_APP_API_URL;

  // Get or set the user session when the component mounts
  useEffect(() => {
    let sessionCookie = Cookies.get("PHPSESSID");
    if (!sessionCookie) {
      const uniqueSession = Math.random().toString(36).substr(2, 9);
      Cookies.set("PHPSESSID", uniqueSession, { path: "/", secure: true, sameSite: "Lax" });
      sessionCookie = uniqueSession;
    }
    setUserSession(sessionCookie);
  }, []);

  const isValidInstagramUrl = (url) => {
    const regex = /^(https?:\/\/)?(www\.)?(instagram\.com)\/.+/;
    return regex.test(url);
  };

  const handleDownload = async () => {
    if (!url) {
      setNotification({
        open: true,
        message: "Please enter an Instagram URL.",
        severity: "error",
      });
      return;
    }

    if (!isValidInstagramUrl(url)) {
      setNotification({
        open: true,
        message: "Invalid Instagram URL. Please provide a valid URL.",
        severity: "error",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${API_URL}instagram/download`,
        { url }
      );

      setVideoInfo({
        filePath: response.data.file_path,
        thumbnail: `${API_URL}${response.data.thumbnail}`,
        title: response.data.title || "Instagram Video",
      });

      setNotification({
        open: true,
        message: response.data.message,
        severity: "success",
      });
      setShowRating(true); // Mostrar componente de calificación después de la descarga
    } catch (error) {
      console.error(error.response?.data?.detail || error.message);
      setNotification({
        open: true,
        message:
          error.response?.data?.detail ||
          "An error occurred while processing your request.",
        severity: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Header />

      <Container sx={{ marginTop: "50px" }}>
        <Typography variant="h4" align="center" gutterBottom>
          Download Instagram Videos
        </Typography>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 2,
            maxWidth: "600px",
            margin: "0 auto",
          }}
        >
          <TextField
            label="Instagram URL"
            variant="outlined"
            fullWidth
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <Button
            variant="contained"
            color="primary"
            size="large"
            fullWidth
            onClick={handleDownload}
            disabled={loading}
            startIcon={loading && <CircularProgress size={20} />}
            sx={{ marginBottom: 3 }}
          >
            {loading ? "Downloading..." : "Download"}
          </Button>
        </Box>

        {videoInfo && (
          <Card
            sx={{
              marginTop: 3,
              maxWidth: 600,
              margin: "0 auto",
              boxShadow: 3,
              borderRadius: 2,
            }}
          >
            <CardMedia
              component="img"
              image={videoInfo.thumbnail}
              alt={videoInfo.title}
              sx={{
                height: "auto",
                width: "100%",
                objectFit: "cover",
              }}
            />
            <CardContent sx={{ textAlign: "center" }}>
              <Typography
                variant="h6"
                component="div"
                sx={{
                  fontWeight: "bold",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
              >
                {videoInfo.title}
              </Typography>
            </CardContent>
            <CardActions
              sx={{
                justifyContent: "center",
                paddingBottom: 2,
                marginTop: 2,
              }}
            >
              <Button
                variant="contained"
                color="success"
                onClick={async () => {
                  try {
                    const response = await fetch(
                      `${API_URL}instagram/download/file?file_path=${encodeURIComponent(
                        videoInfo.filePath
                      )}`
                    );
                    if (!response.ok) {
                      throw new Error("Failed to download file");
                    }
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = videoInfo.filePath;
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    window.URL.revokeObjectURL(url);
                    setShowRating(true); // Mostrar calificación después de descargar
                  } catch (error) {
                    console.error("Download failed:", error);
                  }
                }}
              >
                Download
              </Button>
            </CardActions>
          </Card>
        )}

        {showRating && (
          <Box sx={{ marginTop: 3, textAlign: "center" }}>
            <RatingComponent userSession={userSession} downloadType="instagram" />
          </Box>
        )}

        <Snackbar
          open={notification.open}
          autoHideDuration={6000}
          onClose={() => setNotification({ ...notification, open: false })}
        >
          <Alert
            onClose={() => setNotification({ ...notification, open: false })}
            severity={notification.severity}
            sx={{ width: "100%" }}
          >
            {notification.message}
          </Alert>
        </Snackbar>
      </Container>
    </>
  );
};

export default InstagramModule;
