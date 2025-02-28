import React, { useState, useEffect } from "react";
import Header from "../components/Header"; // Import Header
import Cookies from "js-cookie"; // Import js-cookie to manage cookies
import RatingComponent from "./RatingComponent"; // Import Rating Component
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

const SoundCloudModule = () => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({
    open: false,
    message: "",
    severity: "success",
  });
  const [trackInfo, setTrackInfo] = useState(null);
  const [showRating, setShowRating] = useState(false); // Show rating after download
  const [userSession, setUserSession] = useState(null); // State to store user session

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


  const isValidSoundCloudUrl = (url) => {
    const regex = /^(https?:\/\/)?(www\.)?(soundcloud\.com)\/.+/;
    return regex.test(url);
  };

  const handleDownload = async () => {
    if (!url) {
      setNotification({
        open: true,
        message: "Please enter a SoundCloud URL.",
        severity: "error",
      });
      return;
    }

    if (!isValidSoundCloudUrl(url)) {
      setNotification({
        open: true,
        message: "Invalid SoundCloud URL. Please provide a valid URL.",
        severity: "error",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/soundcloud/download",
        {
          url,
        }
      );

      setTrackInfo({
        filePath: response.data.file_path,
        thumbnail: `http://127.0.0.1:5000${response.data.thumbnail}`, // Complete URL for the thumbnail
        title: response.data.title || "SoundCloud Track",
      });

      setNotification({
        open: true,
        message: response.data.message,
        severity: "success",
      });
      setShowRating(true); // Show rating component
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
          Download SoundCloud Tracks
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
            label="SoundCloud URL"
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

        {trackInfo && (
          <Card
            sx={{
              marginTop: 3,
              maxWidth: 600,
              margin: "0 auto",
              boxShadow: 3,
              borderRadius: 2,
            }}
          >
            {trackInfo.thumbnail && (
              <CardMedia
                component="img"
                image={trackInfo.thumbnail}
                alt={trackInfo.title}
                sx={{
                  height: "auto",
                  width: "100%",
                  objectFit: "cover",
                }}
              />
            )}
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
                {trackInfo.title}
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
                      `http://127.0.0.1:5000/soundcloud/download/file?file_path=${encodeURIComponent(
                        trackInfo.filePath
                      )}`
                    );
                    if (!response.ok) {
                      throw new Error("Failed to download file");
                    }
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = trackInfo.filePath.split("/").pop();
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    window.URL.revokeObjectURL(url);
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

        {showRating && <RatingComponent userSession={userSession} downloadType="soundcloud" />}

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

export default SoundCloudModule;
