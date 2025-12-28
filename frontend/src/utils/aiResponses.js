// Mock AI response generator for private reflection
export function getAIResponse(message, partner, conversationHistory = []) {
    const lowerMessage = message.toLowerCase();

    // Partner A responses - empathetic mirroring
    const partnerAResponses = {
        overwhelmed: "It sounds like you're carrying a lot right now. Feeling overwhelmed during this time is completely normal—your body and mind are going through significant changes. What you're experiencing doesn't mean anything is wrong with you or your relationship.",
        tired: "Physical and emotional exhaustion during pregnancy is incredibly common. Your body is doing extraordinary work, and that takes a real toll. This fatigue isn't a reflection of your effort or care.",
        anxious: "The uncertainty and changes you're facing can naturally bring up anxiety. These feelings are a normal response to a major life transition, not a sign that something is wrong with you.",
        sad: "Feeling sad or down during this time doesn't mean you're failing or that you don't care. Hormonal shifts and life changes can affect mood in ways that have nothing to do with love or commitment.",
        default: "Thank you for sharing that with me. What you're feeling is valid. During pregnancy and postpartum, emotional changes are expected and normal. These feelings don't define your relationship or your capacity to care."
    };

    // Partner B responses - reframing without blame
    const partnerBResponses = {
        confused: "It's understandable to feel confused when your partner's emotions seem different. What might look like distance or lack of interest is often the result of hormonal and physical changes—not a reflection of their feelings for you.",
        frustrated: "Feeling frustrated when communication feels harder is natural. The emotional shifts happening aren't about you or the relationship—they're part of a biological process that affects mood and energy in real ways.",
        worried: "Your concern shows how much you care. What you're noticing in your partner's behavior is likely connected to the significant changes their body and mind are going through, not a sign that something is wrong between you.",
        distant: "When your partner seems distant, it can feel personal. But emotional withdrawal during this time is often a symptom of exhaustion and hormonal changes, not a choice or a message about the relationship.",
        default: "I hear you. It's hard when things feel different. The changes you're seeing in your partner are often tied to pregnancy and postpartum adjustments—not to how they feel about you or your relationship."
    };

    const responses = partner === 'A' ? partnerAResponses : partnerBResponses;

    // Simple keyword matching
    if (lowerMessage.includes('overwhelm') || lowerMessage.includes('too much')) {
        return responses.overwhelmed || responses.default;
    }
    if (lowerMessage.includes('tired') || lowerMessage.includes('exhaust') || lowerMessage.includes('sleep')) {
        return responses.tired || responses.default;
    }
    if (lowerMessage.includes('anxious') || lowerMessage.includes('worry') || lowerMessage.includes('scared')) {
        return responses.anxious || responses.worried || responses.default;
    }
    if (lowerMessage.includes('sad') || lowerMessage.includes('cry') || lowerMessage.includes('depress')) {
        return responses.sad || responses.default;
    }
    if (lowerMessage.includes('confus') || lowerMessage.includes('don\'t understand')) {
        return responses.confused || responses.default;
    }
    if (lowerMessage.includes('frustrat') || lowerMessage.includes('angry')) {
        return responses.frustrated || responses.default;
    }
    if (lowerMessage.includes('distant') || lowerMessage.includes('away') || lowerMessage.includes('withdrawn')) {
        return responses.distant || responses.default;
    }

    return responses.default;
}

// Generate neutral summary from private chat for group chat
export function generateNeutralSummary(partner, messages) {
    const summaries = {
        A: "Partner A has been experiencing emotional overwhelm and fatigue. They've shared feelings of being stretched thin and struggling with energy levels. These experiences are consistent with normal pregnancy-related changes.",
        B: "Partner B has noticed changes in communication and connection. They've expressed concern about emotional distance and are seeking to understand what's happening. Their observations reflect common partner experiences during this transition."
    };

    return summaries[partner] || "This partner has been processing the emotional changes happening during this time.";
}
