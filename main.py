import os
from dotenv import load_dotenv #env files
import feedparser
import requests #sends HTTPS requests to external APIs
from transformers import pipeline   #performing sentiment analysis on text

# Load environment variables from .env file
load_dotenv()

# Initialize sentiment analysis pipeline
pipe = pipeline('sentiment-analysis')

# Get the API key and other variables from environment variables
api_key = os.getenv('API_KEY')
ticker = os.getenv('TICKER')
keyword = os.getenv('KEYWORD')

# Get stock data for Meta Platforms (META) from Finnhub API
# Formulate the API URL to fetch real-time stock data
stock_api_url = f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}'
response = requests.get(stock_api_url)


# if response.status_code == 200:
#     #if successful, parse JSON response and extract stock data
#     data = response.json()
#     #printing stock data
#     print(f"Stock Data for {keyword}:\n")
#     print(f"Current Price: {data['c']}\n")
#     print(f"High Price of the day: {data['h']}\n")
#     print(f"Low Price of the day: {data['l']}\n")
#     print(f"Open Price of the day: {data['o']}\n")
#     print(f"Previous Close Price: {data['pc']}\n")
# else:
#     print(f"Error fetching data: {response.status_code}")

# Fetch the RSS feed for news articles related to the keyword 'META'
rss_feed_url = f"https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US:en"
rss_response = requests.get(rss_feed_url)

# Parse the RSS feed using feedparser
feed = feedparser.parse(rss_response.text)

print(f"\n Found {len(feed.entries)} news articles for '{keyword}':\n")
    
total_score = 0
num_articles = 0

for entry in feed.entries:
    #printing article title, link, date, and summary
    print(f'Title: {entry.title}\n')
    print(f'Link: {entry.link}\n')
    print(f'Published: {entry.published}\n')
    print(f'Summary: {entry.summary}\n')

    #performance of sentiment analysis on article summary
    sentiment = pipe(entry.summary)[0]

    if sentiment["label"] == "NEGATIVE":
        sentiment_score = -sentiment["score"]
    else:
        sentiment_score = sentiment["score"]

    # Print the sentiment label (Positive, Negative, or Neutral) and the score
    print(f'Sentiment {sentiment["label"]}, Score: {sentiment_score}')
    print('-' * 40)

    if sentiment['label'] == 'POSITIVE':
        total_score += sentiment_score
        num_articles += 1   # Count the number of articles with negative sentiment
    elif sentiment['label'] == 'NEGATIVE':
        total_score += sentiment_score
        num_articles += 1   # add because sentiment_score is already negative
    elif sentiment['label'] == 'NEGATIVE':
        num_articles += 1

# Calculate and print the overall sentiment based on the average score
if num_articles > 0:
    final_score = total_score / num_articles

    print("\nSentiment scores range from -1 (negative) to +1 (positive).\n")

    # Threshold adjusted slightly for more accurate classification of neutral cases
    if final_score >= 0.15:
        print(f'Overall Sentiment: Positive {final_score}\n')
    elif final_score <= -0.15:
        print(f'Overall Sentiment: Negative {final_score}\n')
    else:
        print(f'Overall Sentiment: Neutral {final_score}\n')
else:
    print("No articles matched the keyword.")


if response.status_code == 200:
    #if successful, parse JSON response and extract stock data
    data = response.json()
    #printing stock data
    print(f"Stock Data for {keyword}:\n")
    print(f"Current Price: {data['c']}\n")
    print(f"High Price of the day: {data['h']}\n")
    print(f"Low Price of the day: {data['l']}\n")
    print(f"Open Price of the day: {data['o']}\n")
    print(f"Previous Close Price: {data['pc']}\n")
else:
    print(f"Error fetching data: {response.status_code}")