from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


def _id() -> str:
    return str(uuid.uuid4())


@dataclass
class Conversation:
    id: str
    user_id: str
    type: str = "private"
    status: str = "open"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Message:
    id: str
    conversation_id: str
    author_type: str
    content: str
    redaction_state: str = "raw"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Summary:
    id: str
    conversation_id: str
    user_id: str
    summary_text: str
    themes: List[str] = field(default_factory=list)
    confidence: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Consent:
    id: str
    user_id: str
    scope: str
    target_partner_id: Optional[str] = None
    status: str = "granted"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PartnerInsight:
    id: str
    source_summary_id: str
    viewer_partner_id: str
    content: str
    redactions: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Screening:
    id: str
    user_id: str
    instrument: str
    answers: Dict[str, Any]
    score_meta: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ScreeningTrend:
    id: str
    user_id: str
    window: str
    status: str
    flags: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RiskEvent:
    id: str
    user_id: str
    source: str
    level: str
    reason_codes: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Session:
    id: str
    type: str
    participants: List[str]
    allowed_context_ids: List[str]
    status: str = "preparing"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AuditLog:
    id: str
    actor: str
    action: str
    payload_meta: Dict[str, Any]
    risk_level: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class User:
    id: str
    email: str
    password_hash: str
    name: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PartnerLinkRecord:
    id: str
    user_id: str
    partner_user_id: Optional[str]
    status: str = "pending"
    token: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class InMemoryStore:
    def __init__(self) -> None:
        self.conversations: Dict[str, Conversation] = {}
        self.messages: Dict[str, List[Message]] = {}
        self.summaries: Dict[str, Summary] = {}
        self.consents: List[Consent] = []
        self.partner_insights: List[PartnerInsight] = []
        self.screenings: List[Screening] = []
        self.trends: List[ScreeningTrend] = []
        self.risk_events: List[RiskEvent] = []
        self.sessions: Dict[str, Session] = {}
        self.audit_logs: List[AuditLog] = []
        self.users: List[User] = []
        self.partner_links: List[PartnerLinkRecord] = []
        self.tokens: Dict[str, str] = {}  # token -> user_id

    # Conversation and messages
    def create_conversation(self, user_id: str, conv_type: str = "private") -> Conversation:
        conv = Conversation(id=_id(), user_id=user_id, type=conv_type)
        self.conversations[conv.id] = conv
        self.messages[conv.id] = []
        return conv

    def latest_conversation_for_user(self, user_id: str) -> Conversation | None:
        for conv in reversed(list(self.conversations.values())):
            if conv.user_id == user_id:
                return conv
        return None

    def add_message(self, conversation_id: str, author_type: str, content: str) -> Message:
        msg = Message(id=_id(), conversation_id=conversation_id, author_type=author_type, content=content)
        self.messages.setdefault(conversation_id, []).append(msg)
        return msg

    def list_messages(self, conversation_id: str, limit: int = 50) -> List[Message]:
        return self.messages.get(conversation_id, [])[-limit:]

    # Summaries
    def add_summary(self, conversation_id: str, user_id: str, summary_text: str, themes: List[str], confidence: int) -> Summary:
        summ = Summary(id=_id(), conversation_id=conversation_id, user_id=user_id, summary_text=summary_text, themes=themes, confidence=confidence)
        self.summaries[summ.id] = summ
        return summ

    def latest_summaries(self, user_id: str, limit: int = 5) -> List[Summary]:
        return [s for s in self.summaries.values() if s.user_id == user_id][-limit:]

    # Consents
    def grant_consent(self, user_id: str, scope: str, target_partner_id: Optional[str]) -> Consent:
        consent = Consent(id=_id(), user_id=user_id, scope=scope, target_partner_id=target_partner_id, status="granted")
        self.consents.append(consent)
        return consent

    def revoke_consent(self, user_id: str, scope: str, target_partner_id: Optional[str]) -> Consent:
        consent = Consent(id=_id(), user_id=user_id, scope=scope, target_partner_id=target_partner_id, status="revoked")
        self.consents.append(consent)
        return consent

    def list_consents(self, user_id: str) -> List[Consent]:
        return [c for c in self.consents if c.user_id == user_id and c.status == "granted"]

    def is_consent_granted(self, user_id: str, scope: str, target_partner_id: Optional[str]) -> bool:
        for c in reversed(self.consents):
            if c.user_id == user_id and c.scope == scope and c.target_partner_id == target_partner_id:
                return c.status == "granted"
        return False

    # Insights
    def add_partner_insight(self, summary: Summary, viewer_partner_id: str) -> PartnerInsight:
        insight = PartnerInsight(id=_id(), source_summary_id=summary.id, viewer_partner_id=viewer_partner_id, content=summary.summary_text)
        self.partner_insights.append(insight)
        return insight

    def list_insights(self, viewer_id: str) -> List[PartnerInsight]:
        return [i for i in self.partner_insights if i.viewer_partner_id == viewer_id]

    # Screening and risk
    def add_screening(self, user_id: str, instrument: str, answers: Dict[str, Any], score_meta: Dict[str, Any]) -> Screening:
        screening = Screening(id=_id(), user_id=user_id, instrument=instrument, answers=answers, score_meta=score_meta)
        self.screenings.append(screening)
        return screening

    def list_screenings(self, user_id: str, limit: int = 20) -> List[Screening]:
        return [s for s in self.screenings if s.user_id == user_id][-limit:]

    def add_trend(self, user_id: str, window: str, status: str, flags: List[str]) -> ScreeningTrend:
        trend = ScreeningTrend(id=_id(), user_id=user_id, window=window, status=status, flags=flags)
        self.trends.append(trend)
        return trend

    def add_risk_event(self, user_id: str, source: str, level: str, reason_codes: List[str]) -> RiskEvent:
        event = RiskEvent(id=_id(), user_id=user_id, source=source, level=level, reason_codes=reason_codes)
        self.risk_events.append(event)
        return event

    # Escalation sessions
    def create_session(self, participants: List[str], allowed_context_ids: List[str]) -> Session:
        session = Session(id=_id(), type="ai_counselor", participants=participants, allowed_context_ids=allowed_context_ids, status="ready")
        self.sessions[session.id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)

    # Audit
    def add_audit(self, actor: str, action: str, payload_meta: Dict[str, Any], risk_level: str) -> AuditLog:
        log = AuditLog(id=_id(), actor=actor, action=action, payload_meta=payload_meta, risk_level=risk_level)
        self.audit_logs.append(log)
        return log

    # Users and auth tokens
    def add_user(self, email: str, password_hash: str, name: str | None = None) -> User:
        user = User(id=_id(), email=email.lower(), password_hash=password_hash, name=name)
        self.users.append(user)
        return user

    def find_user_by_email(self, email: str) -> Optional[User]:
        email = email.lower()
        return next((u for u in self.users if u.email == email), None)

    def store_token(self, token: str, user_id: str) -> None:
        self.tokens[token] = user_id

    def get_user_by_token(self, token: str) -> Optional[User]:
        uid = self.tokens.get(token)
        if not uid:
            return None
        return next((u for u in self.users if u.id == uid), None)

    # Partner linking
    def create_partner_link(self, user_id: str, token: str) -> PartnerLinkRecord:
        rec = PartnerLinkRecord(id=_id(), user_id=user_id, partner_user_id=None, status="pending", token=token)
        self.partner_links.append(rec)
        return rec

    def accept_partner_link(self, token: str, partner_user_id: str) -> Optional[PartnerLinkRecord]:
        for rec in self.partner_links:
            if rec.token == token and rec.status == "pending":
                rec.partner_user_id = partner_user_id
                rec.status = "linked"
                return rec
        return None

    def partner_status(self, user_id: str) -> Optional[PartnerLinkRecord]:
        return next((r for r in self.partner_links if r.user_id == user_id or r.partner_user_id == user_id), None)

    def linked_partner_id(self, user_id: str) -> Optional[str]:
        rec = self.partner_status(user_id)
        if not rec or rec.status != "linked":
            return None
        return rec.partner_user_id if rec.user_id == user_id else rec.user_id


store = InMemoryStore()


def get_store() -> InMemoryStore:
    return store
