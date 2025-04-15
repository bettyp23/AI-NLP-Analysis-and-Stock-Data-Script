# AI-Powered Sentiment Analysis and Stock Data Script

This script utilizes **Artificial Intelligence (AI)** to perform **sentiment analysis** on news articles related to **Meta Platforms (META)** while also fetching **real-time stock data** for a comprehensive analysis. By leveraging **HuggingFace's transformers library** for sentiment classification and the **Finnhub API** for stock data, this script demonstrates how AI can be used to gain insights from text data and real-time market trends.

---

## **Objective**  

The goal of this project is to demonstrate how **AI** can be used to analyze the sentiment of news articles about **Meta Platforms (META)** and combine this information with real-time stock data for a comprehensive analysis of market sentiment and trends.

---

## **Key Technologies Used**  

- **Artificial Intelligence (AI)**
- **Natural Language Processing (NLP)**
- **HuggingFace Transformers Library**
- **Finnhub API**
- **Python Libraries**: `requests`, `feedparser`, `transformers`

---

## **How AI is Involved**  

### **Sentiment Analysis (NLP/AI)**

- **AI Model**: Utilizes a **pre-trained sentiment analysis model** from HuggingFace, based on **transformer architectures** (e.g., **BERT**, **DistilBERT**).
- **AI Function**: Analyzes news articles and classifies the sentiment as **positive**, **negative**, or **neutral** with a **sentiment score** that measures the strength of the sentiment.
- **Real-World Application**: Helps efficiently process large volumes of news articles and gain insights into public perception about Meta Platforms.

### **Sentiment Classification**

- For each article, the AI model processes the **summary** and outputs a **sentiment label** (positive, negative, neutral) and a **sentiment score** indicating the strength of the sentiment.
- **Goal**: This provides an **intuitive, automated way** to evaluate public sentiment surrounding Meta Platforms.

### **Transformer Models**

- The AI leverages **BERT** or **DistilBERT**, state-of-the-art transformer models capable of capturing **contextual relationships** between words to make accurate sentiment predictions.

---

## **Script Workflow**

### 1. **Fetching Stock Data**

- **API**: Retrieves real-time stock data for **Meta Platforms (META)** using the **Finnhub API**.
- **Metrics**: Includes **current price**, **high**, **low**, **open**, and **previous close** prices.

### 2. **Fetching News Articles**

- **Source**: The script fetches an **RSS feed** from **Google News** related to **Meta Platforms**.
- **Data Extracted**: Each article’s **title**, **link**, **publication date**, and **summary** are captured.

### 3. **Sentiment Analysis of News Articles**

- **Analysis**: The **summary** of each article is processed by the AI-powered sentiment analysis model.
- **Outputs**: The model assigns a **sentiment label** (positive, negative, neutral) and a **sentiment score** to each article.

### 4. **Final Sentiment Calculation**

- **Sentiment Aggregation**: After processing all articles, the script calculates an **average sentiment score** based on articles with **negative sentiment**.
- **Overall Classification**: The overall sentiment of the news feed is classified as **positive**, **negative**, or **neutral**.

---

## **Outcome**

- The script provides a **comprehensive sentiment analysis** of news related to **Meta Platforms (META)** in real-time.
- It outputs:
  - **Sentiment classification** (positive, negative, neutral) for each article.
  - **Sentiment score** indicating the strength of sentiment for each article.
  - An **overall sentiment classification** for the entire news feed.