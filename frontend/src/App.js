import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import TikTokModule from "./pages/TikTokModule";
import YouTubeModule from "./pages/DownloadModule";
import InstagramModule from "./pages/InstagramModule";
import SoundCloudModule from "./pages/SoundCloudModule";
import TwitterModule from "./pages/TwitterModule";
import FacebookModule from "./pages/FacebookModule";
import Footer from "./components/Footer";
import Cookies from "js-cookie";
import TermsAndConditions from "./pages/TermsAndConditions";

const App = () => {
  const [showTerms, setShowTerms] = useState(false);
  const [userSession, setUserSession] = useState(null);

  useEffect(() => {
    // Get or create session cookie
    let sessionCookie = Cookies.get("PHPSESSID");
    if (!sessionCookie) {
      const uniqueSession = Math.random().toString(36).substr(2, 9);
      Cookies.set("PHPSESSID", uniqueSession, { path: "/", secure: true, sameSite: "Lax" });
      sessionCookie = uniqueSession;
    }
    setUserSession(sessionCookie);

    // Check if terms are accepted
    const termsAccepted = Cookies.get("termsAccepted");
    if (!termsAccepted) {
      setShowTerms(true);
    }
  }, []);

  const handleAcceptTerms = () => {
    Cookies.set("termsAccepted", "true", { path: "/", secure: true, sameSite: "Lax" });
    setShowTerms(false);
  };

  const withFooter = (Component) => (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <div style={{ flex: 1 }}>
        <Component userSession={userSession} />
      </div>
      <Footer />
    </div>
  );

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/youtube" element={withFooter(YouTubeModule)} />
          <Route path="/tiktok" element={withFooter(TikTokModule)} />
          <Route path="/instagram" element={withFooter(InstagramModule)} />
          <Route path="/soundcloud" element={withFooter(SoundCloudModule)} />
          <Route path="/twitter" element={withFooter(TwitterModule)} />
          <Route path="/facebook" element={withFooter(FacebookModule)} />
          {/* Standalone Terms and Conditions page */}
          <Route
              path="/terms-and-conditions"
              element={withFooter(() => <TermsAndConditions standalone />)}
            />
          </Routes>
      </Router>

      {showTerms && <TermsAndConditions open={showTerms} onAccept={handleAcceptTerms} />}
    </>
  );
};

export default App;
