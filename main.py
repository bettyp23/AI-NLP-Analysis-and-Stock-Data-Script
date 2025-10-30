"""
AI-Powered Sentiment Analysis and Stock Data Script

This script performs sentiment analysis on news articles related to a specified
company while fetching real-time stock data for comprehensive analysis.
"""

import os
import sys
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv
import feedparser
import requests
from transformers import pipeline

# Constants
SENTIMENT_THRESHOLD_POSITIVE = 0.15
SENTIMENT_THRESHOLD_NEGATIVE = -0.15
REQUEST_TIMEOUT = 30  # seconds
STOCK_DATA_URL = "https://finnhub.io/api/v1/quote"
GOOGLE_NEWS_RSS_BASE = "https://news.google.com/rss/search"


class OutputFormatter:
    """Handles all CLI output formatting for a professional appearance."""
    
    @staticmethod
    def header(title: str, width: int = 70) -> None:
        """Print a formatted header."""
        border = "=" * width
        padding = (width - len(title) - 2) // 2
        print(f"\n{border}")
        print(f"{' ' * padding} {title} {' ' * padding}")
        print(f"{border}\n")
    
    @staticmethod
    def section(title: str, width: int = 70) -> None:
        """Print a section header."""
        print(f"\n{'-' * width}")
        print(f"  {title}")
        print(f"{'-' * width}\n")
    
    @staticmethod
    def separator(width: int = 70) -> None:
        """Print a separator line."""
        print(f"{'-' * width}\n")
    
    @staticmethod
    def info(message: str, indent: int = 0) -> None:
        """Print an info message."""
        print(f"{' ' * indent}[*] {message}")
    
    @staticmethod
    def success(message: str, indent: int = 0) -> None:
        """Print a success message."""
        print(f"{' ' * indent}[+] {message}")
    
    @staticmethod
    def error(message: str, indent: int = 0) -> None:
        """Print an error message."""
        print(f"{' ' * indent}[-] {message}")
    
    @staticmethod
    def progress(current: int, total: int, item: str = "Processing") -> None:
        """Print progress indicator."""
        percentage = int((current / total) * 100)
        bar_length = 30
        filled = int(bar_length * current / total)
        bar = "?" * filled + "?" * (bar_length - filled)
        print(f"\r{item}: [{bar}] {current}/{total} ({percentage}%)", end="", flush=True)
        if current == total:
            print()  # New line when complete
    
    @staticmethod
    def stock_card(ticker: str, data: Dict) -> None:
        """Print stock data in a card format."""
        current = data.get('c', 0)
        change = data.get('d', 0)
        change_pct = data.get('dp', 0)
        change_symbol = "+" if change >= 0 else "-"
        
        print(f"\n+{'=' * 68}+")
        print(f"|  Stock Data: {ticker:<53}|")
        print(f"+{'=' * 68}+")
        print(f"|  Current Price:        ${current:>10,.2f}                    |")
        print(f"|  Previous Close:        ${data.get('pc', 0):>10,.2f}                    |")
        print(f"|  Change:                {change_symbol} ${abs(change):>9,.2f} ({abs(change_pct):>5.2f}%)           |")
        print(f"+{'-' * 68}+")
        print(f"|  High (Today):          ${data.get('h', 0):>10,.2f}                    |")
        print(f"|  Low (Today):           ${data.get('l', 0):>10,.2f}                    |")
        print(f"|  Open (Today):          ${data.get('o', 0):>10,.2f}                    |")
        print(f"+{'=' * 68}+\n")
    
    @staticmethod
    def article_card(num: int, total: int, article: Dict, sentiment: Dict) -> None:
        """Print article analysis in a card format."""
        label = sentiment['label']
        score = sentiment['normalized_score']
        
        # Sentiment indicator
        if label == "POSITIVE":
            indicator = "[+] POSITIVE"
        elif label == "NEGATIVE":
            indicator = "[-] NEGATIVE"
        else:
            indicator = "[ ] NEUTRAL"
        
        # Format date
        published = article.get('published', 'N/A')
        if len(published) > 30:
            published = published[:27] + "..."
        
        # Truncate summary
        summary = article.get('summary', '')
        if len(summary) > 150:
            summary = summary[:147] + "..."
        
        print(f"\n?{'?' * 68}?")
        print(f"?  Article {num}/{total:<58}?")
        print(f"?{'?' * 68}?")
        title = article.get('title', 'N/A')
        if len(title) > 55:
            title = title[:52] + "..."
        print(f"?  Title:   {title:<55}?")
        print(f"?  Date:    {published:<55}?")
        print(f"?  Sentiment: {indicator:<20} Score: {score:>7.4f}          ?")
        if summary:
            print(f"?  Summary:                                               ?")
            # Word wrap summary
            words = summary.split()
            line = "?          "
            for word in words:
                if len(line + word) > 66:
                    print(f"{line:<70}?")
                    line = "?          " + word + " "
                else:
                    line += word + " "
            if line.strip() != "?":
                print(f"{line:<70}?")
        print(f"?{'?' * 68}?")
    
    @staticmethod
    def sentiment_summary(total: int, overall_label: str, overall_score: float, 
                         sentiment_scores: List[float]) -> None:
        """Print sentiment analysis summary."""
        positive_count = sum(1 for s in sentiment_scores if s > 0)
        negative_count = sum(1 for s in sentiment_scores if s < 0)
        neutral_count = sum(1 for s in sentiment_scores if s == 0)
        
        # Create visual bars
        max_count = max(positive_count, negative_count, neutral_count, 1)
        pos_bar = "#" * int((positive_count / max_count) * 20)
        neg_bar = "#" * int((negative_count / max_count) * 20)
        neu_bar = "#" * int((neutral_count / max_count) * 20)
        
        # Pad bars to exactly 20 characters
        pos_bar = pos_bar.ljust(20)
        neg_bar = neg_bar.ljust(20)
        neu_bar = neu_bar.ljust(20)
        
        print(f"\n+{'=' * 68}+")
        print(f"|  Sentiment Analysis Summary{' ' * 40}|")
        print(f"+{'=' * 68}+")
        print(f"|  Articles Analyzed:     {total:>6}                                    |")
        print(f"|  Overall Sentiment:      {overall_label:<12} Score: {overall_score:>7.4f}      |")
        print(f"+{'-' * 68}+")
        print(f"|  Distribution:                                           |")
        print(f"|    Positive:  {positive_count:>4}  [{pos_bar}] ({positive_count*100//total:>3}%) |")
        print(f"|    Negative:  {negative_count:>4}  [{neg_bar}] ({negative_count*100//total:>3}%) |")
        print(f"|    Neutral:   {neutral_count:>4}  [{neu_bar}] ({neutral_count*100//total:>3}%) |")
        print(f"+{'=' * 68}+\n")


class StockDataFetcher:
    """Handles fetching and processing stock data from Finnhub API."""
    
    def __init__(self, api_key: str, ticker: str):
        self.api_key = api_key
        self.ticker = ticker
        
    def fetch_stock_data(self) -> Optional[Dict]:
        """
        Fetch real-time stock data from Finnhub API.
        
        Returns:
            Dictionary containing stock data or None if fetch fails
        """
        if not self.api_key or not self.ticker:
            OutputFormatter.error("API key or ticker symbol is missing.")
            return None
            
        try:
            url = f"{STOCK_DATA_URL}?symbol={self.ticker}&token={self.api_key}"
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate response structure
            if 'c' not in data:
                OutputFormatter.error(f"Invalid stock data response for {self.ticker}")
                return None
                
            return data
            
        except requests.exceptions.Timeout:
            OutputFormatter.error(f"Request timeout while fetching stock data for {self.ticker}")
            return None
        except requests.exceptions.RequestException as e:
            OutputFormatter.error(f"Error fetching stock data: {e}")
            return None
        except json.JSONDecodeError:
            OutputFormatter.error("Invalid JSON response from stock API")
            return None
    
    def format_stock_data(self, data: Dict) -> None:
        """Format and print stock data using OutputFormatter."""
        if not data:
            OutputFormatter.error("Stock data unavailable.")
            return
        OutputFormatter.stock_card(self.ticker, data)


class NewsAnalyzer:
    """Handles fetching news articles and performing sentiment analysis."""
    
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.sentiment_pipeline = None
        
    def initialize_sentiment_model(self):
        """Initialize the sentiment analysis pipeline (lazy loading)."""
        if self.sentiment_pipeline is None:
            OutputFormatter.info("Loading AI sentiment analysis model...")
            try:
                self.sentiment_pipeline = pipeline('sentiment-analysis')
                OutputFormatter.success("Model loaded successfully")
            except Exception as e:
                OutputFormatter.error(f"Error loading sentiment model: {e}")
                sys.exit(1)
    
    def clean_html(self, text: str) -> str:
        """Remove HTML tags and decode HTML entities from text."""
        if not text:
            return ''
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Decode common HTML entities
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        text = text.replace('&nbsp;', ' ')
        # Clean up extra whitespace
        text = ' '.join(text.split())
        return text
    
    def fetch_news_articles(self) -> List[Dict]:
        """
        Fetch news articles from Google News RSS feed.
        
        Returns:
            List of article dictionaries
        """
        if not self.keyword:
            print("Error: Keyword is missing.")
            return []
            
        try:
            url = f"{GOOGLE_NEWS_RSS_BASE}?q={self.keyword}&hl=en-US&gl=US&ceid=US:en"
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            feed = feedparser.parse(response.text)
            
            articles = []
            for entry in feed.entries:
                # Clean HTML from summary
                summary = self.clean_html(entry.get('summary', ''))
                articles.append({
                    'title': self.clean_html(entry.get('title', 'No title')),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': summary
                })
                
            return articles
            
        except requests.exceptions.Timeout:
            OutputFormatter.error("Request timeout while fetching news articles")
            return []
        except requests.exceptions.RequestException as e:
            OutputFormatter.error(f"Error fetching news articles: {e}")
            return []
        except Exception as e:
            OutputFormatter.error(f"Error parsing RSS feed: {e}")
            return []
    
    def analyze_sentiment(self, text: str) -> Optional[Dict]:
        """
        Analyze sentiment of a text string.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with label and score, or None if analysis fails
        """
        if not text or not text.strip():
            return {'label': 'NEUTRAL', 'score': 0.0, 'normalized_score': 0.0}
            
        try:
            self.initialize_sentiment_model()
            result = self.sentiment_pipeline(text)[0]
            
            # Normalize sentiment score
            label = result['label']
            score = result['score']
            
            # Convert NEGATIVE to negative score
            if label == "NEGATIVE":
                normalized_score = -score
            else:
                normalized_score = score
                
            return {
                'label': label,
                'score': score,
                'normalized_score': normalized_score
            }
            
        except Exception as e:
            OutputFormatter.error(f"Error analyzing sentiment: {e}")
            return None


class SentimentAggregator:
    """Handles aggregation and calculation of overall sentiment."""
    
    def __init__(self, positive_threshold: float = SENTIMENT_THRESHOLD_POSITIVE,
                 negative_threshold: float = SENTIMENT_THRESHOLD_NEGATIVE):
        self.positive_threshold = positive_threshold
        self.negative_threshold = negative_threshold
        
    def calculate_overall_sentiment(self, sentiment_scores: List[float]) -> Tuple[str, float]:
        """
        Calculate overall sentiment from a list of sentiment scores.
        
        Args:
            sentiment_scores: List of normalized sentiment scores
            
        Returns:
            Tuple of (sentiment_label, average_score)
        """
        if not sentiment_scores:
            return ("NEUTRAL", 0.0)
            
        average_score = sum(sentiment_scores) / len(sentiment_scores)
        
        if average_score >= self.positive_threshold:
            label = "POSITIVE"
        elif average_score <= self.negative_threshold:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"
            
        return (label, average_score)


def validate_environment() -> Tuple[str, str, str]:
    """
    Validate and retrieve environment variables.
    
    Returns:
        Tuple of (api_key, ticker, keyword)
        
    Raises:
        SystemExit if required variables are missing or invalid
    """
    load_dotenv()
    
    api_key = os.getenv('API_KEY', '').strip()
    ticker = os.getenv('TICKER', '').strip()
    keyword = os.getenv('KEYWORD', '').strip()
    
    # Check for missing or placeholder values
    missing = []
    placeholder_patterns = ['your_', 'your ', 'replace', 'example', 'placeholder', 'xxx', 'test_']
    
    # Validate API_KEY
    if not api_key:
        missing.append('API_KEY')
    elif any(pattern in api_key.lower() for pattern in placeholder_patterns):
        missing.append('API_KEY')
        print(f"Debug: API_KEY appears to be a placeholder: '{api_key[:20]}...'")
    
    # Validate TICKER
    if not ticker:
        missing.append('TICKER')
    elif ticker.startswith('#'):
        missing.append('TICKER')
    
    # Validate KEYWORD
    if not keyword:
        missing.append('KEYWORD')
    elif keyword.startswith('#'):
        missing.append('KEYWORD')
        
    if missing:
        print(f"Error: Missing or invalid environment variables: {', '.join(missing)}")
        print("\nPlease configure your .env file with valid values:")
        print("  API_KEY=your_actual_finnhub_api_key")
        print("  TICKER=META  (or another ticker symbol)")
        print("  KEYWORD=Meta Platforms  (or another search term)")
        print("\nCurrent values detected:")
        print(f"  API_KEY: {'(empty)' if not api_key else api_key[:20] + '...' if len(api_key) > 20 else api_key}")
        print(f"  TICKER: {ticker if ticker else '(empty)'}")
        print(f"  KEYWORD: {keyword if keyword else '(empty)'}")
        print("\nGet your Finnhub API key at: https://finnhub.io/")
        print("\nNote: Make sure your .env file doesn't have spaces around the '=' sign")
        print("      Correct: API_KEY=abc123xyz")
        print("      Wrong:   API_KEY = abc123xyz")
        sys.exit(1)
        
    return api_key, ticker, keyword


def print_article_analysis(article: Dict, sentiment: Dict, num: int, total: int) -> None:
    """Print formatted article analysis using OutputFormatter."""
    OutputFormatter.article_card(num, total, article, sentiment)


def save_results_to_json(results: Dict, filename: str = None):
    """Save analysis results to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sentiment_analysis_{timestamp}.json"
        
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        OutputFormatter.success(f"Results saved to: {filename}")
    except Exception as e:
        OutputFormatter.error(f"Error saving results: {e}")


def main():
    """Main execution function."""
    OutputFormatter.header("AI-Powered Stock Sentiment Analysis", width=70)
    
    # Validate environment variables
    try:
        api_key, ticker, keyword = validate_environment()
    except SystemExit:
        return
    
    # Initialize components
    stock_fetcher = StockDataFetcher(api_key, ticker)
    news_analyzer = NewsAnalyzer(keyword)
    sentiment_aggregator = SentimentAggregator()
    
    # Fetch stock data
    OutputFormatter.section("Stock Data")
    OutputFormatter.info(f"Fetching real-time data for {ticker}...")
    stock_data = stock_fetcher.fetch_stock_data()
    if stock_data:
        stock_fetcher.format_stock_data(stock_data)
    else:
        OutputFormatter.error("Stock data unavailable. Continuing with news analysis...")
    
    # Fetch news articles
    OutputFormatter.section("News Articles")
    OutputFormatter.info(f"Searching for articles about '{keyword}'...")
    articles = news_analyzer.fetch_news_articles()
    
    if not articles:
        OutputFormatter.error("No articles found. Exiting.")
        return
        
    OutputFormatter.success(f"Found {len(articles)} news articles")
    
    # Analyze sentiment for each article
    OutputFormatter.section("Sentiment Analysis")
    OutputFormatter.info("Analyzing article sentiment using AI model...")
    
    sentiment_scores = []
    analysis_results = []
    
    # Show compact progress for each article
    for i, article in enumerate(articles, 1):
        OutputFormatter.progress(i, len(articles), "Analyzing articles")
        
        sentiment = news_analyzer.analyze_sentiment(article['summary'])
        
        if sentiment:
            sentiment_scores.append(sentiment['normalized_score'])
            analysis_results.append({
                'title': article['title'],
                'link': article['link'],
                'published': article['published'],
                'sentiment_label': sentiment['label'],
                'sentiment_score': sentiment['normalized_score']
            })
    
    print()  # Blank line after progress
    
    # Show detailed article cards (first 10 only to avoid clutter)
    max_display = min(10, len(articles))
    OutputFormatter.info(f"Displaying detailed analysis for first {max_display} articles:")
    
    for i in range(max_display):
        if i < len(analysis_results):
            article = articles[i]
            sentiment = {
                'label': analysis_results[i]['sentiment_label'],
                'normalized_score': analysis_results[i]['sentiment_score']
            }
            print_article_analysis(article, sentiment, i + 1, len(articles))
    
    if len(articles) > max_display:
        OutputFormatter.info(f"... and {len(articles) - max_display} more articles (see JSON export for full details)")
    
    # Calculate overall sentiment
    OutputFormatter.section("Analysis Summary")
    
    if sentiment_scores:
        overall_label, overall_score = sentiment_aggregator.calculate_overall_sentiment(sentiment_scores)
        OutputFormatter.sentiment_summary(len(sentiment_scores), overall_label, overall_score, sentiment_scores)
        
        # Prepare results for saving
        results = {
            'timestamp': datetime.now().isoformat(),
            'keyword': keyword,
            'ticker': ticker,
            'stock_data': stock_data,
            'total_articles': len(articles),
            'overall_sentiment': overall_label,
            'overall_score': overall_score,
            'articles': analysis_results
        }
        
        # Optionally save to JSON
        print("[*] Export Options:")
        save_choice = input("    Save results to JSON file? (y/n): ").lower().strip()
        if save_choice == 'y':
            save_results_to_json(results)
            OutputFormatter.success("Analysis complete!")
        else:
            OutputFormatter.success("Analysis complete!")
    else:
        OutputFormatter.error("No articles were successfully analyzed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
