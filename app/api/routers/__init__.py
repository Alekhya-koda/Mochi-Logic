from .auth import router as auth_router
from .consents import router as consents_router
from .conversations import router as conversations_router
from .escalations import router as escalations_router
from .insights import router as insights_router
from .messages import router as messages_router
from .partners import router as partners_router
from .risk_events import router as risk_events_router
from .screenings import router as screenings_router
from .summaries import router as summaries_router

__all__ = [
    "auth_router",
    "consents_router",
    "conversations_router",
    "escalations_router",
    "insights_router",
    "messages_router",
    "partners_router",
    "risk_events_router",
    "screenings_router",
    "summaries_router",
]
