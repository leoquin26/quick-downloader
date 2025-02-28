import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Container,
} from "@mui/material";
import Header from "../components/Header"; // Import Header

const TermsAndConditions = ({ open, onAccept, standalone }) => {
  const content = (
    <div>
      <Typography variant="body1" gutterBottom>
        Welcome to our website. By accessing and using our services, you agree to comply with the following terms
        and conditions. Please read them carefully before proceeding.
      </Typography>
      <Typography variant="h6" gutterBottom>
        1. General Usage
      </Typography>
      <Typography variant="body2" gutterBottom>
        - You agree not to use the service for any illegal or unauthorized purposes.
        <br />
        - You must not attempt to bypass, hack, or misuse the website in any way.
      </Typography>
      <Typography variant="h6" gutterBottom>
        2. Content and Downloads
      </Typography>
      <Typography variant="body2" gutterBottom>
        - This service is for personal use only. Any downloaded content must comply with copyright laws and local
        regulations.
        <br />
        - We are not responsible for how you use the downloaded content.
      </Typography>
      <Typography variant="h6" gutterBottom>
        3. Privacy
      </Typography>
      <Typography variant="body2" gutterBottom>
        - We use cookies to enhance your user experience and provide personalized content. By using this website,
        you consent to our cookie policy.
        <br />
        - Any data collected is handled in accordance with our Privacy Policy.
      </Typography>
      <Typography variant="h6" gutterBottom>
        4. Limitations of Liability
      </Typography>
      <Typography variant="body2" gutterBottom>
        - We do not guarantee uninterrupted access to our services and are not liable for any damages caused by
        service disruptions.
      </Typography>
      <Typography variant="h6" gutterBottom>
        5. Changes to Terms
      </Typography>
      <Typography variant="body2" gutterBottom>
        - These terms may be updated at any time without prior notice. Continued use of the service indicates your
        acceptance of the updated terms.
      </Typography>
      <Typography variant="h6" gutterBottom>
        6. Governing Law
      </Typography>
      <Typography variant="body2" gutterBottom>
        - These terms and conditions are governed by the laws of your jurisdiction. It is your responsibility to
        ensure compliance with local regulations.
      </Typography>
    </div>
  );

  if (standalone) {
    // Render the terms as a full page
    return (
        <>
            <Header />
            <Container sx={{ padding: "2rem" }}>
                <Typography variant="h4" gutterBottom>
                Terms and Conditions
                </Typography>
                {content}
            </Container>
        </>
      
    );
  }

  // Render the terms inside a modal
  return (
    <Dialog open={open} onClose={() => {}} maxWidth="md" fullWidth>
      <DialogTitle>Terms and Conditions</DialogTitle>
      <DialogContent dividers>{content}</DialogContent>
      <DialogActions>
        <Button onClick={onAccept} color="primary" variant="contained">
          Accept
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default TermsAndConditions;
