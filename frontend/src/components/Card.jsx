import './Card.css';

export default function Card({ children, className = '', hover = false }) {
    return (
        <div className={`card-component ${hover ? 'card-hover' : ''} ${className}`}>
            {children}
        </div>
    );
}
