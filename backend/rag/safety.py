import re

MEDICAL_DISCLAIMER = (
    "**Disclaimer:** This response is for educational purposes only and is not "
    "a substitute for professional medical advice, diagnosis, or treatment. "
    "Always consult a licensed healthcare provider for medical decisions."
)

EMERGENCY_PATTERNS = [
    r"\bchest pain\b",
    r"\bcan(?:'t|not) breathe\b",
    r"\bdifficulty breathing\b",
    r"\bshortness of breath\b",
    r"\bstroke\b",
    r"\bface droop(?:ing)?\b",
    r"\bslurred speech\b",
    r"\bunconscious\b",
    r"\bpassed out\b",
    r"\bsevere bleeding\b",
    r"\bsuicid(?:al|e)\b",
    r"\bheart attack\b",
    r"\bseizure\b",
    r"\banaphyla(?:xis|ctic)\b",
    r"\boverdose\b",
    r"\b911\b",
    r"\bemergency room\b",
]


def is_emergency_query(query: str) -> bool:
    normalized = query.lower()
    return any(re.search(pattern, normalized) for pattern in EMERGENCY_PATTERNS)


def get_emergency_response() -> str:
    return (
        "Your message may describe a medical emergency. "
        "**Call your local emergency number immediately (e.g. 911 in the US, 112 in the EU, 102/108 in India)** "
        "or go to the nearest emergency department. Do not wait for an online assessment.\n\n"
        f"{MEDICAL_DISCLAIMER}"
    )


def append_disclaimer(response: str) -> str:
    if MEDICAL_DISCLAIMER in response:
        return response
    return f"{response.rstrip()}\n\n{MEDICAL_DISCLAIMER}"
