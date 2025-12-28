import { useState, useEffect, useRef } from 'react';
import Button from './Button';
import { groupChatScript } from '../utils/groupChatScript';
import { speak, isTTSSupported } from '../utils/tts';
import './GroupChat.css';

export default function GroupChat({ user }) {
    const [messages, setMessages] = useState([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [isComplete, setIsComplete] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        // Auto-advance through counselor messages
        if (currentStep < groupChatScript.length) {
            const timer = setTimeout(() => {
                const scriptMessage = groupChatScript[currentStep];
                setMessages(prev => [...prev, {
                    id: Date.now(),
                    sender: 'counselor',
                    text: scriptMessage.message,
                    type: scriptMessage.type,
                    ttsEnabled: scriptMessage.ttsEnabled
                }]);
                setCurrentStep(currentStep + 1);

                if (currentStep === groupChatScript.length - 1) {
                    setIsComplete(true);
                }
            }, currentStep === 0 ? 500 : 2000);

            return () => clearTimeout(timer);
        }
    }, [currentStep]);

    const handleTTS = (text) => {
        speak(text);
    };

    return (
        <div className="group-chat fade-in">
            <div className="chat-header">
                <div className="header-content">
                    <div className="group-badge">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                            <circle cx="9" cy="7" r="4" />
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                        </svg>
                        <span>Group Conversation</span>
                    </div>
                </div>
            </div>

            <div className="chat-messages">
                <div className="welcome-message">
                    <h3>Welcome to Your Shared Space</h3>
                    <p>This conversation is guided by an AI counselor to help you both understand what's happening emotionally.</p>
                </div>

                {messages.map(msg => (
                    <div key={msg.id} className={`message ${msg.sender}`}>
                        {msg.sender === 'counselor' && (
                            <div className="counselor-avatar">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                                    <circle cx="12" cy="7" r="4" />
                                </svg>
                            </div>
                        )}
                        <div className="message-content">
                            {msg.sender === 'counselor' && (
                                <div className="message-sender">AI Counselor</div>
                            )}
                            <div className="message-bubble">
                                {msg.text}
                            </div>
                            {msg.ttsEnabled && isTTSSupported() && (
                                <button
                                    className="tts-button"
                                    onClick={() => handleTTS(msg.text)}
                                    title="Listen to this message"
                                >
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
                                        <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07" />
                                    </svg>
                                    Listen
                                </button>
                            )}
                        </div>
                    </div>
                ))}

                {isComplete && (
                    <div className="completion-message">
                        <h4>✓ Conversation Complete</h4>
                        <p>You can return to your private reflection spaces anytime. Take care of yourselves.</p>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>
        </div>
    );
}
