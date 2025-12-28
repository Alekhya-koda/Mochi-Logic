import Button from './Button';
import Card from './Card';
import './ConsentModal.css';

export default function ConsentModal({ onAccept, onDecline }) {
    return (
        <div className="consent-modal-overlay fade-in">
            <Card className="consent-modal">
                <h2>Group Conversation Invitation</h2>

                <div className="consent-content">
                    <p className="consent-intro">
                        Based on your screening results, we'd like to invite you to a guided
                        conversation with your partner and our AI counselor.
                    </p>

                    <div className="consent-section">
                        <h4>What will be shared:</h4>
                        <ul>
                            <li>✓ Neutral summaries of your emotional experiences</li>
                            <li>✓ General patterns we've observed</li>
                            <li>✓ Your screening results (score only)</li>
                        </ul>
                    </div>

                    <div className="consent-section">
                        <h4>What stays private:</h4>
                        <ul>
                            <li>🔒 Your specific private chat messages</li>
                            <li>🔒 Personal details you haven't chosen to share</li>
                            <li>🔒 Individual question responses</li>
                        </ul>
                    </div>

                    <div className="consent-notice">
                        <p>
                            <strong>This is a safe, non-judgmental space.</strong> The AI counselor
                            will help you both understand what's happening emotionally—not diagnose,
                            prescribe, or judge.
                        </p>
                    </div>
                </div>

                <div className="consent-actions">
                    <Button onClick={onAccept}>
                        I Consent - Join Conversation
                    </Button>
                    <Button variant="secondary" onClick={onDecline}>
                        Not Right Now
                    </Button>
                </div>
            </Card>
        </div>
    );
}
