# TODO (Codex Vibe Coding MVP Demo)

## Stack
- Vite + React + Tailwind
- Local mock data only (no backend)
- Demo-grade auth + partner linking (front-end only)

## Core Flow + UX
- Lock demo flow: Partner A reflection -> EPDS -> escalation -> group chat -> close
- Define minimal UI screens: private chat, EPDS survey, risk result, consent modal, group chat
- Draft key AI prompts: reflection, EPDS interpretation, escalation invite, group chat opener/closer

## App Scaffold + Core Flows (Frontend Only)
- Scaffold app with Vite + React + Tailwind
- Build screen shell + routing/state machine for demo flow
- Implement demo auth + partner linking (single screen + in-memory state)
- Implement private chat (Partner A/B) with role separation
- Implement EPDS survey (10 items, 0–3) and scoring
- Implement risk signal logic:
  - EPDS >=13, or EPDS >=10 twice, or sustained irritability + loss of interest
- Store results in local state with privacy separation (private vs shared)

## Escalation + Group Chat
- Build consent gate for group chat; share neutral summaries only
- Implement AI counselor escalation trigger + invite
- Implement group chat UI and AI mediation responses
- Add present-moment alignment script (safety -> shared mapping -> needs -> close)

## Voice + Polish
- Stub TTS (button + placeholder audio; integrate ElevenLabs only if keys available)
- Add language safeguards (non-clinical, non-prescriptive)
- Run full end-to-end demo; fix UX gaps
- Prepare demo script + rehearsal checklist

## Implementation Notes (Codex)
- Keep all flows client-side; no network calls required
- Use mock AI responses (hardcoded scripts) aligned to the demo scenario
- Ensure the demo can be driven start-to-finish in under 5 minutes

## Demo Readiness Checklist
- Partner A reflection works and shows empathetic mirroring
- Partner B reflection reframes misinterpretation without blame
- EPDS completes, scores, and triggers risk signal
- Consent is explicit; private data stays private
- Group chat runs and ends with shared understanding summary
- Optional TTS plays for closing summary

