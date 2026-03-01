# scoring_engine.py

positive_words = ["good", "excellent", "love", "amazing", "best"]
negative_words = ["bad", "terrible", "hate", "worst"]

def calculate_score(text):
    score = 0
    for word in text.split():
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1
    return score