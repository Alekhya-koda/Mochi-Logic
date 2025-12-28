// AI Counselor script for group chat mediation
export const groupChatScript = [
    {
        id: 1,
        speaker: "counselor",
        message: "Hello, I'm here to help you both understand what's been happening emotionally. This is a safe space to explore these changes together. Before we begin, I want to check in—do you both feel comfortable continuing this conversation right now?",
        type: "safety_check"
    },
    {
        id: 2,
        speaker: "counselor",
        message: "Thank you. I've reviewed the summaries from your individual reflections. Let me share what I'm seeing:\n\n• Partner A has been experiencing emotional overwhelm and fatigue—common responses to the physical and hormonal changes of pregnancy.\n\n• Partner B has noticed changes in connection and is seeking to understand what's happening.\n\nThese are both normal experiences during this transition. Neither of you is doing anything wrong.",
        type: "shared_mapping"
    },
    {
        id: 3,
        speaker: "counselor",
        message: "What's important to understand is that emotional changes during pregnancy and postpartum are biological responses—not choices or messages about the relationship. Partner A, your fatigue and overwhelm aren't signs of failure. Partner B, the distance you're noticing isn't about you.",
        type: "pattern_awareness"
    },
    {
        id: 4,
        speaker: "counselor",
        message: "Right now, what do each of you need most from this moment together? Not what you need to fix or change—just what would help you feel more understood.",
        type: "needs_identification"
    },
    {
        id: 5,
        speaker: "counselor",
        message: "Thank you both for being here and for being open to understanding each other. Here's what I want you to take away:\n\n✓ The emotional changes you're experiencing are normal and expected\n✓ They're not about love, effort, or the strength of your relationship\n✓ You're both navigating this transition in your own ways, and that's okay\n\nYou can return to your private reflection spaces anytime. I'm here when you need support.",
        type: "closing_summary",
        ttsEnabled: true
    }
];

// Get next message in the script
export function getNextCounselorMessage(currentStep) {
    if (currentStep < groupChatScript.length) {
        return groupChatScript[currentStep];
    }
    return null;
}

// Generate partner response prompts
export function getPartnerPrompt(step, partner) {
    const prompts = {
        1: {
            A: "You can respond with how you're feeling right now, or simply say 'yes' to continue.",
            B: "You can respond with how you're feeling right now, or simply say 'yes' to continue."
        },
        4: {
            A: "Take a moment to think about what would help you feel understood right now.",
            B: "Take a moment to think about what would help you feel understood right now."
        }
    };

    return prompts[step]?.[partner] || "";
}
