# Plan

## Objectives (per PRD)
- Web app that helps couples interpret emotional/psychological changes together during pregnancy and postpartum.
- Reduce misinterpretation of emotional changes as lack of care or relationship failure via a shared framework.
- Provide neutral, non-judgmental individual reflection spaces with regular depression screening to surface early signals.
- When risk is detected, enable a group conversation supported by an AI counselor using non-clinical language and strong privacy.

## Non-Goals (per PRD)
- No diagnosis, treatment, or crisis intervention.
- Not a replacement for therapy or medical care; no deep relationship counseling.
- No prescriptive behavioral advice; output is understanding, not action plans.

## Audience
- Primary: Couples in pregnancy/postpartum experiencing emotional or relational strain who want clarity and mutual understanding.
- Secondary: None in MVP; no human therapist involvement.

## Constraints
- MVP is web-based and built for a 2-day hackathon.
- Each partner uses a private chat flow individually.
- Regular depression screening for each partner; monitored over time; strictly non-diagnostic language.
- Escalation is triggered and occasional (AI counselor-led only), not continuous.
- High standards for privacy, neutrality, and emotional safety.
- No human therapist involvement in MVP.
- Group chat stays in present-moment alignment; no deep history exploration in MVP.

## Key Use Cases to Deliver
- Individual emotional reflection by each partner with contextualized prompts.
- Regular depression screening and monitoring over time.
- Interpretation of emotional changes with a shared framework and summaries to restore alignment after misalignment.
- Detection of emotional risk or depression signals.
- Escalation to a group chat supported by an AI counselor.

## Scope (MVP)
- Partner account/linking with private chat experiences and empathetic, neutral prompts.
- EPDS survey flow (10 items, 0–3 scoring) and basic risk flagging (non-diagnostic).
- Risk signal definition: EPDS >=13, or EPDS >=10 twice, or sustained irritability + loss of interest indicators across surveys.
- Shared interpretive summaries/mental models to reduce misinterpretation (clarity, not advice).
- Escalation workflow into an AI counselor-supported group chat with necessary context.
- Explicit consent for group chat; only neutral summaries are shared and private chats remain private.
- Language safeguards to keep interactions neutral and non-clinical.
- TTS output for key AI responses (demo-grade).

## Out-of-Scope (MVP)
- Emergency/911-style workflows or live crisis support.
- Any human therapist involvement.
- Prescriptive behavioral or relationship advice; deep counseling features.

## Success Criteria
- Partners report clearer mutual understanding and fewer misinterpretations (>75% positive surveys).
- Regular screenings completed weekly by both partners (>70% adherence).
- Faster recovery of shared understanding after misalignment (self-reported 30% improvement).
- Reliable escalation flow into AI counselor-supported group chat; privacy upheld.
- End-to-end demo scenario runs smoothly without manual intervention.

## Milestones & Deliverables (2-Day Hackathon)
- M0 (pre-start): Requirements/PRD alignment finalized (current state).
- M1 (Day 1 AM): Lock core scenario (individual reflection → EPDS → escalation) and UX wireflows.
- M2 (Day 1 PM): Implement individual AI counseling chat, reflection UX, EPDS survey flow, and EPDS scoring + basic risk flags.
- M3 (Day 2 AM): Implement AI counselor escalation behavior and couple group chat experience.
- M4 (Day 2 PM): Integrate TTS for key AI responses; stabilize, polish, and rehearse end-to-end demo.

## Workstreams
- Product/UX: Flows for individual chats, screening cadence, shared summaries, and escalation.
- Content/Behavioral: Non-judgmental prompts, shared emotional language, non-clinical phrasing.
- Data/Safety: EPDS scoring, risk thresholds (non-diagnostic), privacy/consent, auditability.
- Engineering: Web app, auth + partner linking, chat infra, EPDS flow, risk detection, escalation routing, AI counselor integration, TTS integration.
- AI Counselor Experience: Prompt/policy management for reflection, EPDS interpretation, and couple mediation roles.

## Risks & Mitigations
- Perception of diagnosis → Strict non-clinical language, disclaimers, content reviews.
- Low screening adherence → Low-friction prompts/reminders; flexible timing.
- Privacy/trust concerns → Transparent consent, data minimization, access controls.
- No human therapist escalation → Strong disclaimers, non-clinical language, and clear boundaries around support.
- AI counselor missteps or harmful responses → Policy/prompt hardening, red-teaming, fallback escalation to human reviewer in pilot.
- Misaligned summaries causing harm → Conservative summarization; human-in-the-loop during pilot.

## Metrics (early)
- Adoption: Linked partner accounts; onboarding completion.
- Engagement: Weekly screening completion per partner; chat sessions per week.
- Understanding: Clarity/misalignment scores; reduction in “misunderstood” reports.
- Safety: Risk flag rates, false positives/negatives (qualitative in pilot), escalation latency to AI counselor.

## Demo Scenario (MVP)
- Step 1: Partner A private reflection; AI provides empathetic mirroring and optional, non-prescriptive framing.
- Step 2: Partner B private reflection; AI reframes misinterpretation without blame.
- Step 3: EPDS screening for both partners; risk signal generated using defined thresholds.
- Step 4: Escalation invite with explicit consent; neutral summaries only.
- Step 5: AI counselor group chat focused on present-moment alignment (safety, shared mapping, pattern awareness, reflection, naming needs, optional micro-guidance).
- Step 6: Shared understanding restored; AI closes with a brief summary and optional TTS.

## Pilot Plan (Post-Hackathon, Optional)
- Recruit 5–10 couples (first-time parents with reported emotional disconnect).
- Run 4–6 weeks with weekly screenings and shared summaries; track misalignment recovery.
- Trigger AI counselor group chat on risk flags; measure latency and satisfaction.
- Post-pilot debrief on clarity, safety, and trust before scaling.
