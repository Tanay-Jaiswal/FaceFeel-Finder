"""
Very small, deterministic keyword-based sentiment engine.
For production, replace with a real model/service.
"""
from collections import Counter

POSITIVE = [
    "good","great","love","amazing","happy","awesome","nice","super","fantastic",
    "excellent","cool","excited","delight","wow","best","beautiful","helpful","glad",
    "amazing","perfect","smooth","fast","clean","favorite","support","in love",
    "looking forward","can't wait","so good","really good","very good"
]
NEGATIVE = [
    "bad","worst","hate","angry","upset","horrible","disappointed","awful","terrible",
    "poor","sad","pain","annoying","useless","meh","broken","slow","buggy","worried",
    "confusing","hate it","not good","terrible","frustrating","dislike","junk"
]
NEUTRAL_HINTS = [
    "ok","fine","average","whatever","normal","meh","fair","decent","mixed","okay",
    "not bad","not great"
]


def classify(text: str) -> str:
    t = text.lower()
    positive_score = sum(1 for k in POSITIVE if k in t)
    negative_score = sum(1 for k in NEGATIVE if k in t)
    neutral_score = sum(1 for k in NEUTRAL_HINTS if k in t)

    if positive_score > negative_score and positive_score > neutral_score:
        return "positive"
    if negative_score > positive_score and negative_score > neutral_score:
        return "negative"
    if neutral_score > 0:
        return "neutral"
    if positive_score == negative_score and positive_score > 0:
        return "neutral"
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

    