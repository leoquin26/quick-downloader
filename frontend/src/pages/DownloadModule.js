import React, { useState, useEffect } from "react";
import Cookies from "js-cookie"; // Import js-cookie to manage cookies
import Header from "../components/Header"; // Import Header
import RatingComponent from "./RatingComponent"; // Import the Rating Component
import {
  Box,
  Button,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
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

const DownloadModule = () => {
  const [url, setUrl] = useState("");
  const [format, setFormat] = useState("audio");
  const [quality, setQuality] = useState("320kbps");
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: "", severity: "success" });
  const [videoInfo, setVideoInfo] = useState(null);
  const [showRating, setShowRating] = useState(false); // State to control Rating display
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

  const getVideoIdFromUrl = (url) => {
    const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
  };

  const handleDownload = async () => {
    if (!url) {
      setNotification({ open: true, message: "Please enter a YouTube URL.", severity: "error" });
      return;
    }

    const videoId = getVideoIdFromUrl(url);
    if (!videoId) {
      setNotification({ open: true, message: "Invalid YouTube URL.", severity: "error" });
      return;
    }

    setLoading(true);
    try {
      const endpoint = format === "audio" ? "/youtube/download/audio" : "/youtube/download/video";
      const requestData = format === "audio" ? { url, quality } : { url };

      const response = await axios.post(`${API_URL}${endpoint}`, requestData);
      setVideoInfo({
        filePath: response.data.file_path,
        preview: `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`,
        title: response.data.title || "Untitled Video",
      });
      setNotification({ open: true, message: response.data.message, severity: "success" });
      setShowRating(true); // Show Rating after successful download
    } catch (error) {
      console.error(error.response?.data?.detail || error.message);
      setNotification({
        open: true,
        message: error.response?.data?.detail || "An error occurred while processing your request.",
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
          Download Videos & Audio
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
            label="YouTube URL"
            variant="outlined"
            fullWidth
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <FormControl fullWidth>
            <InputLabel>Format</InputLabel>
            <Select value={format} onChange={(e) => setFormat(e.target.value)}>
              <MenuItem value="audio">Audio</MenuItem>
              <MenuItem value="video">Video</MenuItem>
            </Select>
          </FormControl>

          {format === "audio" && (
            <FormControl fullWidth>
              <InputLabel>Quality</InputLabel>
              <Select value={quality} onChange={(e) => setQuality(e.target.value)}>
                <MenuItem value="320kbps">320kbps</MenuItem>
                <MenuItem value="256kbps">256kbps</MenuItem>
                <MenuItem value="128kbps">128kbps</MenuItem>
              </Select>
            </FormControl>
          )}

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
            {loading ? "Converting..." : "Convert"}
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
              image={videoInfo.preview}
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
                      `http://127.0.0.1:5000/youtube/download/file?file_path=${encodeURIComponent(
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
                    link.download = videoInfo.filePath.split("/").pop();
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    window.URL.revokeObjectURL(url);
                    setShowRating(true); // Show Rating after download
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
            <RatingComponent
              userSession={userSession} // Pass user session to RatingComponent
              downloadType="youtube" // Specify download type
              onRatingSubmitted={(rating) => console.log(`Rated ${rating} stars`)}
            />
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

export default DownloadModule;
