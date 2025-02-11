import React, { useState, useEffect } from "react";
import { Box, Typography, Snackbar, Alert } from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import axios from "axios";

const RatingComponent = ({ userSession, downloadType, onRatingSubmitted }) => {
  const [rating, setRating] = useState(0);
  const [hasRated, setHasRated] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: "", severity: "success" });

  // Fetch user rating
  useEffect(() => {
    const fetchUserRating = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/ratings/user", {
          params: { user_session: userSession, download_type: downloadType },
        });
        if (response.data?.rating) {
          setRating(response.data.rating);
          setHasRated(true);
        }
      } catch (error) {
        console.error("Error fetching user rating:", error);
      }
    };

    fetchUserRating();
  }, [userSession, downloadType]);

  const handleRating = async (rate) => {
    try {
      await axios.post("http://127.0.0.1:5000/api/ratings", {
        user_session: userSession,
        download_type: downloadType,
        rating: rate,
      });

      setRating(rate);
      setHasRated(true);
      setNotification({ open: true, message: "Thank you for your feedback!", severity: "success" });

      onRatingSubmitted?.(rate); // Callback to parent
    } catch (error) {
      console.error("Error submitting rating:", error);
      setNotification({ open: true, message: "Failed to submit feedback. Please try again.", severity: "error" });
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 2,
        marginTop: 3,
      }}
    >
      <Typography variant="h6">Rate your experience</Typography>
      <Box sx={{ display: "flex", gap: 1 }}>
        {[1, 2, 3, 4, 5].map((star) => (
          <StarIcon
            key={star}
            onClick={() => !hasRated && handleRating(star)}
            sx={{
              cursor: hasRated ? "default" : "pointer",
              color: star <= rating ? "gold" : "gray",
              fontSize: 40,
            }}
          />
        ))}
      </Box>
      {hasRated && (
        <Typography sx={{ marginTop: 1, color: "green" }}>
          Thank you for rating! <StarIcon sx={{ color: "green", fontSize: 20 }} />
        </Typography>
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
    </Box>
  );
};

export default RatingComponent;
