# sentiment_analyzer.py

positive_words = ["good", "excellent", "love", "amazing", "best", "great"]
negative_words = ["bad", "terrible", "hate", "worst", "poor"]

def analyze_sentiment(text):
    score = 0
    words = text.lower().split()

    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return score, sentiment