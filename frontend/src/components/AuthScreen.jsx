import { useState } from 'react';
import Button from './Button';
import Card from './Card';
import './AuthScreen.css';

export default function AuthScreen({ onAuth }) {
    const [name, setName] = useState('');
    const [partner, setPartner] = useState('');
    const [showPartnerSelect, setShowPartnerSelect] = useState(false);

    const handleNameSubmit = (e) => {
        e.preventDefault();
        if (name.trim()) {
            setShowPartnerSelect(true);
        }
    };

    const handlePartnerSelect = (selectedPartner) => {
        setPartner(selectedPartner);
        onAuth({ name, partner: selectedPartner });
    };

    return (
        <div className="auth-screen fade-in">
            <div className="auth-container">
                <div className="auth-header">
                    <h1 className="auth-title">MocchiLogic</h1>
                    <p className="auth-tagline">Shared understanding for couples during pregnancy and postpartum</p>
                </div>

                {!showPartnerSelect ? (
                    <Card className="auth-card">
                        <form onSubmit={handleNameSubmit}>
                            <div className="form-group">
                                <label htmlFor="name">What's your name?</label>
                                <input
                                    id="name"
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    placeholder="Enter your name"
                                    autoFocus
                                />
                            </div>
                            <Button type="submit" disabled={!name.trim()}>
                                Continue
                            </Button>
                        </form>
                    </Card>
                ) : (
                    <Card className="auth-card">
                        <div className="partner-select">
                            <h3>Welcome, {name}!</h3>
                            <p>Which partner are you?</p>
                            <div className="partner-buttons">
                                <button
                                    className="partner-option"
                                    onClick={() => handlePartnerSelect('A')}
                                >
                                    <div className="partner-label">Partner A</div>
                                    <div className="partner-desc">Experiencing pregnancy/postpartum</div>
                                </button>
                                <button
                                    className="partner-option"
                                    onClick={() => handlePartnerSelect('B')}
                                >
                                    <div className="partner-label">Partner B</div>
                                    <div className="partner-desc">Supporting partner</div>
                                </button>
                            </div>
                        </div>
                    </Card>
                )}

                <div className="auth-disclaimer">
                    <p>🔒 Your private reflections remain completely confidential</p>
                    <p>⚠️ This is not a diagnostic or clinical treatment tool</p>
                </div>
            </div>
        </div>
    );
}
