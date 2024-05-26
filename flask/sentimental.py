import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Get the polarity scores
    scores = sia.polarity_scores(text)
    
    # Determine sentiment
    
    if scores['compound'] > 0 :
        sentiment = "It's great to hear that you're feeling optimistic about the future! Keep focusing on the positive aspects of your life and remember that you're making progress every day."
    elif scores['compound'] < 0:
        sentiment = "I'm sorry to hear that you're feeling down today. It's important to acknowledge and accept your emotions, but also remember that you're not alone and there are people who care about you and want to support you"
    else:
        sentiment = "It sounds like you're feeling a bit neutral about the situation. That's okay! Sometimes we experience a range of emotions, and it's important to take some time to reflect on how you're feeling and what you need in this moment"

    return sentiment, scores['compound']
