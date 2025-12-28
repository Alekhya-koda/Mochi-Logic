import { useState, useEffect, useRef } from 'react';
import Button from './Button';
import TypingIndicator from './TypingIndicator';
import { getAIResponse } from '../utils/aiResponses';
import './PrivateChat.css';

export default function PrivateChat({ user, onComplete }) {
    const [messages, setMessages] = useState([
        {
            id: 1,
            sender: 'ai',
            text: user.partner === 'A'
                ? "Hello. This is your private space to reflect on how you've been feeling. Everything you share here stays completely private. How have you been doing lately?"
                : "Hello. This is your private space to reflect on what you've been noticing. Everything you share here stays completely private. How have things been feeling for you lately?"
        }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = {
            id: messages.length + 1,
            sender: 'user',
            text: input.trim()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // Simulate AI thinking time
        setTimeout(() => {
            const aiResponse = getAIResponse(input, user.partner, messages);
            const aiMessage = {
                id: messages.length + 2,
                sender: 'ai',
                text: aiResponse
            };
            setMessages(prev => [...prev, aiMessage]);
            setIsTyping(false);
        }, 1500);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="private-chat fade-in">
            <div className="chat-header">
                <div className="header-content">
                    <div className="privacy-badge">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                        </svg>
                        <span>Private Space</span>
                    </div>
                    <div className="header-actions">
                        <Button variant="secondary" onClick={onComplete}>
                            Continue to Screening
                        </Button>
                    </div>
                </div>
            </div>

            <div className="chat-messages">
                {messages.map(msg => (
                    <div key={msg.id} className={`message ${msg.sender}`}>
                        <div className="message-bubble">
                            {msg.text}
                        </div>
                    </div>
                ))}
                {isTyping && (
                    <div className="message ai">
                        <div className="message-bubble">
                            <TypingIndicator />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-container">
                <div className="chat-input-wrapper">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Share your thoughts..."
                        rows="1"
                        disabled={isTyping}
                    />
                    <button
                        className="send-button"
                        onClick={handleSend}
                        disabled={!input.trim() || isTyping}
                    >
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <line x1="22" y1="2" x2="11" y2="13" />
                            <polygon points="22 2 15 22 11 13 2 9 22 2" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    );
}
