import { useState } from 'react';
import Button from './Button';
import Card from './Card';
import { epdsQuestions, calculateEPDSScore, detectRisk, interpretScore } from '../utils/epdsLogic';
import './EPDSScreen.css';

export default function EPDSScreen({ user, onComplete }) {
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [answers, setAnswers] = useState({});
    const [showResults, setShowResults] = useState(false);

    const handleAnswer = (value) => {
        const newAnswers = { ...answers, [currentQuestion]: value };
        setAnswers(newAnswers);

        if (currentQuestion < epdsQuestions.length - 1) {
            setTimeout(() => {
                setCurrentQuestion(currentQuestion + 1);
            }, 300);
        } else {
            setTimeout(() => {
                setShowResults(true);
            }, 300);
        }
    };

    const handleBack = () => {
        if (currentQuestion > 0) {
            setCurrentQuestion(currentQuestion - 1);
        }
    };

    const score = calculateEPDSScore(answers);
    const risk = detectRisk(score);
    const interpretation = interpretScore(score);

    if (showResults) {
        return (
            <div className="epds-screen fade-in">
                <div className="epds-container">
                    <Card className="results-card">
                        <h2>Screening Complete</h2>
                        <div className="score-display" style={{ borderColor: interpretation.color }}>
                            <div className="score-number">{score}</div>
                            <div className="score-label">out of 30</div>
                        </div>

                        <div className="interpretation">
                            <p>{interpretation.interpretation}</p>
                        </div>

                        {risk.hasRisk && (
                            <div className="risk-notice">
                                <h4>💙 Support Available</h4>
                                <p>{risk.message}</p>
                                <p className="risk-next-step">
                                    We'd like to invite you and your partner to a guided conversation
                                    with our AI counselor. This is a safe space to explore these changes together.
                                </p>
                            </div>
                        )}

                        <div className="disclaimer">
                            <p><strong>Important:</strong> This screening is not a diagnosis. It's a tool to help you understand how you're feeling and whether additional support might be helpful.</p>
                        </div>

                        <Button onClick={() => onComplete(score, risk)}>
                            {risk.hasRisk ? 'Continue to Next Step' : 'Complete Reflection'}
                        </Button>
                    </Card>
                </div>
            </div>
        );
    }

    const question = epdsQuestions[currentQuestion];
    const progress = ((currentQuestion + 1) / epdsQuestions.length) * 100;

    return (
        <div className="epds-screen fade-in">
            <div className="epds-container">
                <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progress}%` }} />
                </div>

                <Card className="question-card">
                    <div className="question-header">
                        <span className="question-number">Question {currentQuestion + 1} of {epdsQuestions.length}</span>
                    </div>

                    <h3 className="question-text">{question.question}</h3>

                    <div className="options">
                        {question.options.map((option, index) => (
                            <button
                                key={index}
                                className={`option-button ${answers[currentQuestion] === option.value ? 'selected' : ''}`}
                                onClick={() => handleAnswer(option.value)}
                            >
                                {option.label}
                            </button>
                        ))}
                    </div>

                    {currentQuestion > 0 && (
                        <Button variant="secondary" onClick={handleBack}>
                            Back
                        </Button>
                    )}
                </Card>

                <div className="epds-info">
                    <p>🔒 Your responses are private and confidential</p>
                </div>
            </div>
        </div>
    );
}
