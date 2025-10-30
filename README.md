# AI-Powered Sentiment Analysis and Stock Data Script

This script utilizes **Artificial Intelligence (AI)** to perform **sentiment analysis** on news articles related to a specified company while also fetching **real-time stock data** for a comprehensive analysis. By leveraging **HuggingFace's transformers library** for sentiment classification and the **Finnhub API** for stock data, this script demonstrates how AI can be used to gain insights from text data and real-time market trends.

---

## **Objective**  

The goal of this project is to demonstrate how **AI** can be used to analyze the sentiment of news articles about a company and combine this information with real-time stock data for a comprehensive analysis of market sentiment and trends.

---

## **Key Technologies Used**  

- **Artificial Intelligence (AI)**
- **Natural Language Processing (NLP)**
- **HuggingFace Transformers Library**
- **Finnhub API**
- **Python Libraries**: `requests`, `feedparser`, `transformers`, `python-dotenv`

---

## **Features**

### **Core Functionality**
- ✅ Real-time stock data fetching from Finnhub API
- ✅ Automated news article retrieval from Google News RSS feeds
- ✅ AI-powered sentiment analysis using transformer models
- ✅ Comprehensive error handling and validation
- ✅ Progress indicators and formatted output
- ✅ Optional JSON export for results
- ✅ **Professional CLI Interface**: Clean, formatted terminal output with ASCII-compatible characters

### **Recent Improvements**
- 🆕 **Modular Architecture**: Object-oriented design with separate classes for stock data, news analysis, and sentiment aggregation
- 🆕 **Enhanced Error Handling**: Comprehensive try-except blocks, request timeouts, and graceful error recovery
- 🆕 **Input Validation**: Environment variable validation at startup with clear error messages
- 🆕 **Better Statistics**: Detailed score distribution showing positive/negative/neutral article counts
- 🆕 **JSON Export**: Save analysis results to JSON files for later analysis
- 🆕 **Progress Tracking**: Visual progress indicators showing current article being processed
- 🆕 **Code Quality**: Type hints, docstrings, and well-structured code for maintainability

---

## **How AI is Involved**  

### **Sentiment Analysis (NLP/AI)**

- **AI Model**: Utilizes a **pre-trained sentiment analysis model** from HuggingFace, based on **transformer architectures** (e.g., **BERT**, **DistilBERT**).
- **AI Function**: Analyzes news articles and classifies the sentiment as **positive**, **negative**, or **neutral** with a **sentiment score** that measures the strength of the sentiment.
- **Real-World Application**: Helps efficiently process large volumes of news articles and gain insights into public perception about companies.

### **Sentiment Classification**

- For each article, the AI model processes the **summary** and outputs a **sentiment label** (positive, negative, neutral) and a **sentiment score** indicating the strength of the sentiment.
- **Goal**: This provides an **intuitive, automated way** to evaluate public sentiment surrounding companies.

### **Transformer Models**

- The AI leverages **BERT** or **DistilBERT**, state-of-the-art transformer models capable of capturing **contextual relationships** between words to make accurate sentiment predictions.

---

## **Script Workflow**

### 1. **Environment Validation**

- **Validation**: Checks for required environment variables (`API_KEY`, `TICKER`, `KEYWORD`)
- **Error Handling**: Exits gracefully with clear error messages if variables are missing

### 2. **Fetching Stock Data**

- **API**: Retrieves real-time stock data using the **Finnhub API**.
- **Metrics**: Includes **current price**, **high**, **low**, **open**, **previous close**, and **change percentage**.
- **Error Handling**: Continues with news analysis if stock data is unavailable

### 3. **Fetching News Articles**

- **Source**: The script fetches an **RSS feed** from **Google News** related to the specified keyword.
- **Data Extracted**: Each article's **title**, **link**, **publication date**, and **summary** are captured.
- **Error Handling**: Handles timeouts, network errors, and parsing errors gracefully

### 4. **Sentiment Analysis of News Articles**

- **Analysis**: The **summary** of each article is processed by the AI-powered sentiment analysis model.
- **Outputs**: The model assigns a **sentiment label** (positive, negative, neutral) and a **sentiment score** to each article.
- **Progress**: Shows progress indicator for each article being analyzed

### 5. **Final Sentiment Calculation**

- **Sentiment Aggregation**: After processing all articles, the script calculates an **average sentiment score** based on all articles.
- **Overall Classification**: The overall sentiment of the news feed is classified as **positive**, **negative**, or **neutral**.
- **Statistics**: Provides detailed breakdown of positive, negative, and neutral article counts

### 6. **Results Export** (Optional)

- **JSON Export**: Optionally save all results to a timestamped JSON file for later analysis
- **Data Included**: Timestamp, keyword, ticker, stock data, sentiment analysis results, and individual article details

---

## **Setup Instructions**

### **Prerequisites**

**Python 3.8 or higher** is required.

### **Installation**

Install all required dependencies using pip:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install python-dotenv feedparser requests transformers torch
```

**Note**: If you encounter the error `Import "dotenv" could not be resolved`, this means the `python-dotenv` package is not installed. Run the installation command above to fix it.

### **Environment Variables**

Create a `.env` file in the project root with the following variables:

```
API_KEY=your_finnhub_api_key
TICKER=META
KEYWORD=Meta Platforms
```

- **API_KEY**: Your Finnhub API key (get one at [finnhub.io](https://finnhub.io))
- **TICKER**: Stock ticker symbol (e.g., META, AAPL, GOOGL)
- **KEYWORD**: Search keyword for news articles (e.g., "Meta Platforms", "Apple Inc")

### **Running the Script**

```bash
python main.py
```

---

## **Output Example**

```
============================================================
AI-Powered Sentiment Analysis and Stock Data Script
============================================================

Fetching stock data...
Stock Data for META:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Price: $485.23
High Price (today): $489.50
Low Price (today): $482.10
Open Price (today): $483.00
Previous Close: $480.00
Change: $5.23 (1.09%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fetching news articles for 'Meta Platforms'...
Found 10 news articles.

============================================================
Article Analysis
============================================================

[Article 1/10]
Title: Meta Announces New AI Features
Link: https://...
Published: ...
Summary: ...
Sentiment: POSITIVE, Score: 0.8542
────────────────────────────────────────────────────────────

...

============================================================
Overall Sentiment Analysis
============================================================

Analyzed 10 articles
Sentiment scores range from -1 (negative) to +1 (positive)

Overall Sentiment: POSITIVE
Average Score: 0.3421
Score Distribution:
  Positive articles: 7
  Negative articles: 2
  Neutral articles: 1

Save results to JSON file? (y/n):
```

---

## **Outcome**

- The script provides a **comprehensive sentiment analysis** of news related to a specified company in real-time.
- It outputs:
  - **Sentiment classification** (positive, negative, neutral) for each article.
  - **Sentiment score** indicating the strength of sentiment for each article.
  - An **overall sentiment classification** for the entire news feed.
  - **Detailed statistics** showing the distribution of sentiment across articles.
  - **Optional JSON export** for further analysis and record-keeping.

---

## **Architecture**

The script is organized into three main classes:

1. **`StockDataFetcher`**: Handles all stock API operations and data formatting
2. **`NewsAnalyzer`**: Manages news fetching and sentiment analysis (with lazy model loading)
3. **`SentimentAggregator`**: Calculates overall sentiment from individual scores

This modular design makes the code:
- **Testable**: Each component can be tested independently
- **Maintainable**: Clear separation of concerns
- **Extensible**: Easy to add new features or modify existing ones

---

## **Error Handling**

The script includes comprehensive error handling for:
- Missing environment variables
- API request timeouts
- Network connectivity issues
- Invalid API responses
- RSS feed parsing errors
- Sentiment analysis failures

All errors are handled gracefully with informative error messages, allowing the script to continue execution when possible.

---

## **Performance Features**

- **Lazy Loading**: Sentiment analysis model loads only when needed
- **Request Timeouts**: 30-second timeout prevents indefinite hanging
- **Efficient Processing**: All articles processed in a single pass
- **Graceful Degradation**: Continues execution even if some components fail

---

## **License**

This project is provided as-is for educational and demonstration purposes.
