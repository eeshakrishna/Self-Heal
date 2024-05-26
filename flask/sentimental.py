import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def analyze_sentiment(text):
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Get the polarity scores
    scores = sia.polarity_scores(text)
    
    # Return the compound score
    return scores['compound']
