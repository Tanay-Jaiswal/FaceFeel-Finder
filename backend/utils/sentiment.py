"""
Very small, deterministic keyword-based sentiment engine.
For production, replace with a real model/service.
"""
from collections import Counter

POSITIVE = [
    "good","great","love","amazing","happy","awesome","nice","super","fantastic",
    "excellent","cool","excited","looking forward","can't wait","delight","wow"
]
NEGATIVE = [
    "bad","worst","hate","angry","upset","horrible","disappointed","awful","terrible",
    "poor","sad","pain","annoying","useless","meh"
]
NEUTRAL_HINTS = ["ok","fine","average","whatever","normal"]

def classify(text: str) -> str:
    t = text.lower()
    if any(k in t for k in POSITIVE):
        return "positive"
    if any(k in t for k in NEGATIVE):
        return "negative"
    if any(k in t for k in NEUTRAL_HINTS):
        return "neutral"
    # naive default
    return "neutral"

def summarize(comments):
    """
    comments: list of dicts with 'message' key
    returns: dict counts + overall
    """
    counts = Counter({"positive":0,"negative":0,"neutral":0})
    for c in comments:
        msg = (c or {}).get("message","")
        if not msg:
            continue
        label = classify(msg)
        counts[label] += 1
    total = sum(counts.values())
    if total == 0:
        # no messages classified -> fall back to neutral
        overall_emotion = "neutral"
    elif counts["positive"] == counts["negative"]:
        overall_emotion = "neutral"
    else:
        overall_emotion = max(
            ("positive", "negative", "neutral"),
            key=lambda emotion: counts[emotion],
        )

    return {
        "emotion_distribution": dict(counts),
        "overall_emotion": overall_emotion,
        "total_comments": total,
    }

    