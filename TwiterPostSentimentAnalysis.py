import pandas as pd
import re
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Load the dataset with error handling
try:
    df = pd.read_csv('/Users/sohamdhore/Desktop/Projects /Machine_Learning_Miniprojects/Sentiment_analyssisbot/TwiterPostSentimentAnalysis.py', header=None)
    df.columns = ['tweet_id', 'entity', 'original_sentiment', 'text']
    print("Dataset loaded successfully. First few rows:")
    print(df.head())
except FileNotFoundError:
    print("Error: CSV file not found. Check the path.")
    exit()
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Preprocess the text
def preprocess(text):
    text = re.sub(r'http\S+', '', str(text))  # Handle non-string input
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'#\S+', '', text)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

df['clean_text'] = df['text'].apply(preprocess)

# Sentiment analysis with TextBlob
def get_sentiment_textblob(text):
    blob = TextBlob(text)
    if blob.sentiment.polarity > 0:
        return 'positive'
    elif blob.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

df['sentiment_textblob'] = df['clean_text'].apply(get_sentiment_textblob)

# Sentiment analysis with VADER
nltk.download('vader_lexicon', quiet=True)  # Download lexicon quietly
sia = SentimentIntensityAnalyzer()

def get_sentiment_vader(text):
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    if compound > 0:
        return 'positive'
    elif compound < 0:
        return 'negative'
    else:
        return 'neutral'

df['sentiment_vader'] = df['clean_text'].apply(get_sentiment_vader)

# Display sentiment counts
print("\nSentiment counts (TextBlob):")
print(df['sentiment_textblob'].value_counts())
print("\nSentiment counts (VADER):")
print(df['sentiment_vader'].value_counts())

# Visualize sentiment distribution for VADER (you can repeat for TextBlob if needed)
df['sentiment_vader'].value_counts().plot(kind='bar')
plt.title('Sentiment Distribution (VADER)')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Optional: Compare with original sentiment if available
if 'original_sentiment' in df.columns:
    print("\nComparison with original sentiment:")
    print(df[['text', 'original_sentiment', 'sentiment_textblob', 'sentiment_vader']].head())