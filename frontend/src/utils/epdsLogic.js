// Edinburgh Postnatal Depression Scale (EPDS) questions
export const epdsQuestions = [
    {
        id: 1,
        question: "I have been able to laugh and see the funny side of things",
        options: [
            { value: 0, label: "As much as I always could" },
            { value: 1, label: "Not quite so much now" },
            { value: 2, label: "Definitely not so much now" },
            { value: 3, label: "Not at all" }
        ]
    },
    {
        id: 2,
        question: "I have looked forward with enjoyment to things",
        options: [
            { value: 0, label: "As much as I ever did" },
            { value: 1, label: "Rather less than I used to" },
            { value: 2, label: "Definitely less than I used to" },
            { value: 3, label: "Hardly at all" }
        ]
    },
    {
        id: 3,
        question: "I have blamed myself unnecessarily when things went wrong",
        options: [
            { value: 3, label: "Yes, most of the time" },
            { value: 2, label: "Yes, some of the time" },
            { value: 1, label: "Not very often" },
            { value: 0, label: "No, never" }
        ]
    },
    {
        id: 4,
        question: "I have been anxious or worried for no good reason",
        options: [
            { value: 0, label: "No, not at all" },
            { value: 1, label: "Hardly ever" },
            { value: 2, label: "Yes, sometimes" },
            { value: 3, label: "Yes, very often" }
        ]
    },
    {
        id: 5,
        question: "I have felt scared or panicky for no very good reason",
        options: [
            { value: 3, label: "Yes, quite a lot" },
            { value: 2, label: "Yes, sometimes" },
            { value: 1, label: "No, not much" },
            { value: 0, label: "No, not at all" }
        ]
    },
    {
        id: 6,
        question: "Things have been getting on top of me",
        options: [
            { value: 3, label: "Yes, most of the time I haven't been able to cope" },
            { value: 2, label: "Yes, sometimes I haven't been coping as well as usual" },
            { value: 1, label: "No, most of the time I have coped quite well" },
            { value: 0, label: "No, I have been coping as well as ever" }
        ]
    },
    {
        id: 7,
        question: "I have been so unhappy that I have had difficulty sleeping",
        options: [
            { value: 3, label: "Yes, most of the time" },
            { value: 2, label: "Yes, sometimes" },
            { value: 1, label: "Not very often" },
            { value: 0, label: "No, not at all" }
        ]
    },
    {
        id: 8,
        question: "I have felt sad or miserable",
        options: [
            { value: 3, label: "Yes, most of the time" },
            { value: 2, label: "Yes, quite often" },
            { value: 1, label: "Not very often" },
            { value: 0, label: "No, not at all" }
        ]
    },
    {
        id: 9,
        question: "I have been so unhappy that I have been crying",
        options: [
            { value: 3, label: "Yes, most of the time" },
            { value: 2, label: "Yes, quite often" },
            { value: 1, label: "Only occasionally" },
            { value: 0, label: "No, never" }
        ]
    },
    {
        id: 10,
        question: "The thought of harming myself has occurred to me",
        options: [
            { value: 3, label: "Yes, quite often" },
            { value: 2, label: "Sometimes" },
            { value: 1, label: "Hardly ever" },
            { value: 0, label: "Never" }
        ]
    }
];

// Calculate EPDS score
export function calculateEPDSScore(answers) {
    return Object.values(answers).reduce((sum, value) => sum + value, 0);
}

// Detect risk based on EPDS score and history
export function detectRisk(currentScore, previousScores = []) {
    // Risk criteria:
    // 1. EPDS >= 13
    // 2. EPDS >= 10 twice
    // 3. Question 10 (self-harm) > 0

    if (currentScore >= 13) {
        return {
            hasRisk: true,
            reason: "elevated_score",
            message: "Your responses indicate you may be experiencing significant emotional challenges. This is common during pregnancy and postpartum, and support is available."
        };
    }

    const scoresAbove10 = previousScores.filter(s => s >= 10).length;
    if (currentScore >= 10 && scoresAbove10 >= 1) {
        return {
            hasRisk: true,
            reason: "persistent_elevation",
            message: "Your responses show ongoing emotional challenges. Connecting with support could help you navigate this time."
        };
    }

    return {
        hasRisk: false,
        message: "Your responses suggest you're managing the emotional aspects of this transition. Continue to check in with yourself regularly."
    };
}

// Get interpretation of score (non-diagnostic)
export function interpretScore(score) {
    if (score >= 13) {
        return {
            level: "high",
            interpretation: "Your responses suggest you're experiencing significant emotional challenges. This doesn't mean anything is wrong with you—it means you could benefit from additional support during this transition.",
            color: "var(--color-warning)"
        };
    } else if (score >= 10) {
        return {
            level: "moderate",
            interpretation: "Your responses indicate some emotional difficulty. This is a normal part of the changes you're going through, and it's worth keeping an eye on how you're feeling.",
            color: "var(--color-info)"
        };
    } else {
        return {
            level: "low",
            interpretation: "Your responses suggest you're managing the emotional aspects of this time relatively well. Continue to check in with yourself regularly.",
            color: "var(--color-success)"
        };
    }
}
