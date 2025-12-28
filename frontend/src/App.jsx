import { useState } from 'react';
import AuthScreen from './components/AuthScreen';
import PrivateChat from './components/PrivateChat';
import EPDSScreen from './components/EPDSScreen';
import ConsentModal from './components/ConsentModal';
import GroupChat from './components/GroupChat';
import './App.css';

function App() {
  const [currentScreen, setCurrentScreen] = useState('auth');
  const [user, setUser] = useState(null);
  const [epdsScore, setEpdsScore] = useState(null);
  const [hasRisk, setHasRisk] = useState(false);
  const [showConsent, setShowConsent] = useState(false);

  const handleAuth = (userData) => {
    setUser(userData);
    setCurrentScreen('privateChat');
  };

  const handlePrivateChatComplete = () => {
    setCurrentScreen('epds');
  };

  const handleEPDSComplete = (score, risk) => {
    setEpdsScore(score);
    setHasRisk(risk.hasRisk);

    if (risk.hasRisk) {
      setShowConsent(true);
    } else {
      setCurrentScreen('complete');
    }
  };

  const handleConsentAccept = () => {
    setShowConsent(false);
    setCurrentScreen('groupChat');
  };

  const handleConsentDecline = () => {
    setShowConsent(false);
    setCurrentScreen('complete');
  };

  return (
    <div className="app">
      {currentScreen === 'auth' && (
        <AuthScreen onAuth={handleAuth} />
      )}

      {currentScreen === 'privateChat' && (
        <PrivateChat user={user} onComplete={handlePrivateChatComplete} />
      )}

      {currentScreen === 'epds' && (
        <EPDSScreen user={user} onComplete={handleEPDSComplete} />
      )}

      {currentScreen === 'groupChat' && (
        <GroupChat user={user} />
      )}

      {currentScreen === 'complete' && (
        <div className="complete-screen fade-in">
          <div className="complete-container">
            <h1>Thank You</h1>
            <p>You've completed your reflection and screening for today.</p>
            <p className="complete-message">
              Remember: emotional changes during pregnancy and postpartum are normal.
              You're not alone in this journey.
            </p>
          </div>
        </div>
      )}

      {showConsent && (
        <ConsentModal
          onAccept={handleConsentAccept}
          onDecline={handleConsentDecline}
        />
      )}
    </div>
  );
}

export default App;
