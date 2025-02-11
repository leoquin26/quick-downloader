import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#4CAF50",
    },
    secondary: {
      main: "#FFC107",
    },
    background: {
      default: "#F5F5F5",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#212121",
      secondary: "#757575",
    },
  },
  typography: {
    fontFamily: "'Poppins', Arial, sans-serif",
    h1: {
      fontSize: "3rem",
      fontWeight: 600,
    },
    h2: {
      fontSize: "2.5rem",
      fontWeight: 600,
    },
    h5: {
      fontSize: "1.5rem",
      fontWeight: 400,
    },
    body1: {
      fontSize: "1rem",
      lineHeight: 1.6,
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          margin: 0,
          padding: 0,
          width: "100%",
          height: "100%",
          overflowX: "hidden",
          boxSizing: "border-box",
          backgroundColor: "#F5F5F5",
        },
        "#root": {
          height: "100%",
        },
      },
    },
  },
});

export default theme;
