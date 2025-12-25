"""FastAPI entrypoint for the backend (ChatKit route disabled due to agents import issues)."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routers import (
    auth_router,
    consents_router,
    conversations_router,
    escalations_router,
    insights_router,
    messages_router,
    partners_router,
    risk_events_router,
    screenings_router,
    summaries_router,
)

app = FastAPI(title="AI Counselor Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(partners_router)
app.include_router(conversations_router)
app.include_router(messages_router)
app.include_router(summaries_router)
app.include_router(consents_router)
app.include_router(insights_router)
app.include_router(screenings_router)
app.include_router(risk_events_router)
app.include_router(escalations_router)
