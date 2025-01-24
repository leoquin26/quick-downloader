import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import TikTokModule from "./pages/TikTokModule";
import YouTubeModule from "./pages/DownloadModule";
import InstagramModule from "./pages/InstagramModule";
import SoundCloudModule from "./pages/SoundCloudModule";
import Footer from "./components/Footer";

const App = () => {
  const withFooter = (Component) => (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <div style={{ flex: 1 }}>
        <Component />
      </div>
      <Footer />
    </div>
  );

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/youtube" element={withFooter(YouTubeModule)} />
        <Route path="/tiktok" element={withFooter(TikTokModule)} />
        <Route path="/instagram" element={withFooter(InstagramModule)} />
        <Route path="/soundcloud" element={withFooter(SoundCloudModule)} />;
      </Routes>
    </Router>
  );
};

export default App;
