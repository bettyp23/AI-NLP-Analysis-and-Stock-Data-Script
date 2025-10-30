"""
Graphical Desktop Application for Stock Sentiment Analysis

This Tkinter-based GUI application provides a user-friendly interface for
analyzing stock sentiment using AI-powered NLP analysis.

Features:
- Real-time stock data display
- News article listing with sentiment analysis
- Overall sentiment summary and statistics
- Top positive/negative articles
- Investment recommendation (BUY/HOLD/SELL)
- Export to JSON functionality
- Progress tracking and status messages
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os
from dotenv import load_dotenv

# Import existing classes from main.py
from main import (
    StockDataFetcher,
    NewsAnalyzer,
    SentimentAggregator,
    validate_environment,
    save_results_to_json,
    SENTIMENT_THRESHOLD_POSITIVE,
    SENTIMENT_THRESHOLD_NEGATIVE
)


class StockSentimentGUI:
    """
    Main GUI application class for stock sentiment analysis.
    
    This class manages the entire GUI interface, including:
    - Stock data display
    - News article listing
    - Sentiment analysis results
    - User interactions (refresh, export)
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Stock Sentiment Analysis - AI-Powered")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Application state
        self.api_key = None
        self.ticker = None
        self.keyword = None
        self.stock_fetcher = None
        self.news_analyzer = None
        self.sentiment_aggregator = None
        self.current_results = None
        
        # Color scheme for sentiment
        self.colors = {
            'positive': '#4CAF50',  # Green
            'negative': '#F44336',  # Red
            'neutral': '#FFC107',   # Yellow
            'background': '#f0f0f0',
            'frame_bg': '#ffffff',
            'text_dark': '#212121',
            'text_light': '#757575'
        }
        
        # Initialize components
        self._setup_ui()
        self._load_environment()
        
        # Auto-load data on startup
        self.root.after(500, self.refresh_data)
    
    def _setup_ui(self):
        """Set up the user interface components."""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['background'], padx=10, pady=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        self._create_header(main_container)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Stock Data & Summary Tab
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Summary & Stock Data")
        self._create_summary_tab(summary_frame)
        
        # News Articles Tab
        articles_frame = ttk.Frame(notebook)
        notebook.add(articles_frame, text="News Articles")
        self._create_articles_tab(articles_frame)
        
        # Control buttons (always visible)
        self._create_control_buttons(main_container)
        
        # Status bar
        self._create_status_bar(main_container)
    
    def _create_header(self, parent):
        """Create the header section with title and recommendation."""
        header_frame = tk.Frame(parent, bg=self.colors['frame_bg'], relief=tk.RAISED, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="AI-Powered Stock Sentiment Analysis",
            font=('Arial', 18, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark']
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Recommendation label (will be updated dynamically)
        self.recommendation_label = tk.Label(
            header_frame,
            text="Loading...",
            font=('Arial', 14, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark']
        )
        self.recommendation_label.pack(side=tk.RIGHT, padx=15, pady=10)
    
    def _create_summary_tab(self, parent):
        """Create the summary tab with stock data and sentiment overview."""
        # Left panel - Stock Data
        left_panel = tk.Frame(parent, bg=self.colors['background'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        
        # Stock Data Frame
        stock_frame = tk.LabelFrame(
            left_panel,
            text="Real-Time Stock Data",
            font=('Arial', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            padx=10,
            pady=10
        )
        stock_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.stock_data_text = scrolledtext.ScrolledText(
            stock_frame,
            height=15,
            width=50,
            font=('Courier', 10),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.stock_data_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Sentiment Summary
        right_panel = tk.Frame(parent, bg=self.colors['background'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)
        
        # Overall Sentiment Frame
        sentiment_frame = tk.LabelFrame(
            right_panel,
            text="Overall Sentiment Analysis",
            font=('Arial', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            padx=10,
            pady=10
        )
        sentiment_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.sentiment_summary_text = scrolledtext.ScrolledText(
            sentiment_frame,
            height=10,
            width=50,
            font=('Arial', 10),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.sentiment_summary_text.pack(fill=tk.BOTH, expand=True)
        
        # Distribution Frame
        distribution_frame = tk.LabelFrame(
            right_panel,
            text="Sentiment Distribution",
            font=('Arial', 12, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            padx=10,
            pady=10
        )
        distribution_frame.pack(fill=tk.BOTH, expand=True)
        
        self.distribution_text = scrolledtext.ScrolledText(
            distribution_frame,
            height=8,
            width=50,
            font=('Courier', 10),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.distribution_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_articles_tab(self, parent):
        """Create the articles tab with news articles and top lists."""
        # Create paned window for resizable sections
        paned = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - All Articles
        articles_left = ttk.Frame(paned)
        paned.add(articles_left, weight=2)
        
        articles_label = tk.Label(
            articles_left,
            text="Latest News Articles",
            font=('Arial', 12, 'bold'),
            bg=self.colors['background']
        )
        articles_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # Articles listbox with scrollbar
        articles_frame = tk.Frame(articles_left)
        articles_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar_articles = tk.Scrollbar(articles_frame)
        scrollbar_articles.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.articles_listbox = tk.Listbox(
            articles_frame,
            yscrollcommand=scrollbar_articles.set,
            font=('Arial', 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            selectbackground=self.colors['positive'],
            height=25
        )
        self.articles_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_articles.config(command=self.articles_listbox.yview)
        
        # Article details text area
        details_label = tk.Label(
            articles_left,
            text="Article Details",
            font=('Arial', 10, 'bold'),
            bg=self.colors['background']
        )
        details_label.pack(anchor=tk.W, padx=5, pady=(10, 5))
        
        self.article_details_text = scrolledtext.ScrolledText(
            articles_left,
            height=8,
            font=('Arial', 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['text_dark'],
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.article_details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind selection event
        self.articles_listbox.bind('<<ListboxSelect>>', self._on_article_select)
        
        # Right side - Top Articles
        articles_right = ttk.Frame(paned)
        paned.add(articles_right, weight=1)
        
        # Top Positive Articles
        top_positive_frame = tk.LabelFrame(
            articles_right,
            text="Top Positive Articles",
            font=('Arial', 11, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['positive'],
            padx=5,
            pady=5
        )
        top_positive_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.top_positive_listbox = tk.Listbox(
            top_positive_frame,
            font=('Arial', 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['positive'],
            selectbackground=self.colors['positive'],
            height=10
        )
        self.top_positive_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top Negative Articles
        top_negative_frame = tk.LabelFrame(
            articles_right,
            text="Top Negative Articles",
            font=('Arial', 11, 'bold'),
            bg=self.colors['frame_bg'],
            fg=self.colors['negative'],
            padx=5,
            pady=5
        )
        top_negative_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.top_negative_listbox = tk.Listbox(
            top_negative_frame,
            font=('Arial', 9),
            bg=self.colors['frame_bg'],
            fg=self.colors['negative'],
            selectbackground=self.colors['negative'],
            height=10
        )
        self.top_negative_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_control_buttons(self, parent):
        """Create control buttons (Refresh, Export)."""
        button_frame = tk.Frame(parent, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            button_frame,
            text="[Refresh] Refresh Data",
            font=('Arial', 11, 'bold'),
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2',
            activeforeground='white',
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            command=self.refresh_data
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        # Export button
        export_btn = tk.Button(
            button_frame,
            text="?? Export to JSON",
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            activebackground='#388E3C',
            activeforeground='white',
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            command=self.export_to_json
        )
        export_btn.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = tk.Label(
            button_frame,
            textvariable=self.progress_var,
            font=('Arial', 10),
            bg=self.colors['background'],
            fg=self.colors['text_dark']
        )
        progress_label.pack(side=tk.LEFT, padx=20)
        
        self.progress_bar = ttk.Progressbar(
            button_frame,
            mode='indeterminate',
            length=200
        )
        self.progress_bar.pack(side=tk.LEFT, padx=10)
    
    def _create_status_bar(self, parent):
        """Create the status bar at the bottom."""
        status_frame = tk.Frame(parent, bg=self.colors['background'], relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="Ready - Click 'Refresh Data' to start analysis")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            bg=self.colors['background'],
            fg=self.colors['text_light'],
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, padx=5, pady=2)
    
    def _load_environment(self):
        """Load and validate environment variables."""
        try:
            self.api_key, self.ticker, self.keyword = validate_environment()
            self.stock_fetcher = StockDataFetcher(self.api_key, self.ticker)
            self.news_analyzer = NewsAnalyzer(self.keyword)
            self.sentiment_aggregator = SentimentAggregator()
            self._update_status(f"Loaded: {self.ticker} | Keyword: {self.keyword}")
        except SystemExit:
            # Environment validation failed - show error and close
            messagebox.showerror(
                "Configuration Error",
                "Please configure your .env file with valid API_KEY, TICKER, and KEYWORD.\n\n"
                "The application will now close."
            )
            self.root.quit()
    
    def _update_status(self, message: str):
        """Update the status bar message."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def _update_progress(self, message: str, show_bar: bool = False):
        """Update progress indicator."""
        self.progress_var.set(message)
        if show_bar:
            self.progress_bar.start(10)
        else:
            self.progress_bar.stop()
        self.root.update_idletasks()
    
    def refresh_data(self):
        """Refresh stock data and news analysis in a background thread."""
        if not self.stock_fetcher or not self.news_analyzer:
            messagebox.showerror("Error", "Environment not properly configured.")
            return
        
        # Disable refresh button during analysis
        self.refresh_btn_state = tk.DISABLED
        
        # Start analysis in background thread
        thread = threading.Thread(target=self._perform_analysis, daemon=True)
        thread.start()
    
    def _perform_analysis(self):
        """Perform the complete analysis (runs in background thread)."""
        try:
            # Update UI from main thread
            self.root.after(0, lambda: self._update_progress("Fetching stock data...", True))
            self.root.after(0, lambda: self._update_status("Fetching real-time stock data..."))
            
            # Fetch stock data
            stock_data = self.stock_fetcher.fetch_stock_data()
            
            # Update stock display
            self.root.after(0, lambda: self._display_stock_data(stock_data))
            
            # Fetch news articles
            self.root.after(0, lambda: self._update_progress("Fetching news articles...", True))
            self.root.after(0, lambda: self._update_status("Fetching news articles from Google News..."))
            
            articles = self.news_analyzer.fetch_news_articles()
            
            if not articles:
                self.root.after(0, lambda: messagebox.showwarning("Warning", "No articles found."))
                self.root.after(0, lambda: self._update_progress("Ready", False))
                return
            
            # Analyze sentiment
            self.root.after(0, lambda: self._update_progress("Analyzing sentiment...", True))
            self.root.after(0, lambda: self._update_status(f"Analyzing sentiment for {len(articles)} articles..."))
            
            sentiment_scores = []
            analysis_results = []
            
            for i, article in enumerate(articles):
                progress_pct = int((i + 1) / len(articles) * 100)
                self.root.after(0, lambda p=progress_pct: self._update_progress(f"Analyzing articles... {p}%", True))
                
                sentiment = self.news_analyzer.analyze_sentiment(article['summary'])
                
                if sentiment:
                    sentiment_scores.append(sentiment['normalized_score'])
                    analysis_results.append({
                        'title': article['title'],
                        'link': article['link'],
                        'published': article['published'],
                        'summary': article.get('summary', ''),
                        'sentiment_label': sentiment['label'],
                        'sentiment_score': sentiment['normalized_score']
                    })
            
            # Calculate overall sentiment
            overall_label, overall_score = self.sentiment_aggregator.calculate_overall_sentiment(sentiment_scores)
            
            # Store results
            self.current_results = {
                'timestamp': datetime.now().isoformat(),
                'keyword': self.keyword,
                'ticker': self.ticker,
                'stock_data': stock_data,
                'total_articles': len(articles),
                'overall_sentiment': overall_label,
                'overall_score': overall_score,
                'articles': analysis_results
            }
            
            # Update all displays
            self.root.after(0, lambda: self._display_sentiment_summary(overall_label, overall_score, sentiment_scores))
            self.root.after(0, lambda: self._display_articles(analysis_results))
            self.root.after(0, lambda: self._display_top_articles(analysis_results))
            self.root.after(0, lambda: self._update_recommendation(stock_data, overall_score))
            
            # Complete
            self.root.after(0, lambda: self._update_progress("Ready", False))
            self.root.after(0, lambda: self._update_status(f"Analysis complete! Analyzed {len(analysis_results)} articles."))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            self.root.after(0, lambda: self._update_progress("Ready", False))
            self.root.after(0, lambda: self._update_status("Error during analysis."))
    
    def _display_stock_data(self, stock_data: Optional[Dict]):
        """Display stock data in the stock data text area."""
        self.stock_data_text.config(state=tk.NORMAL)
        self.stock_data_text.delete(1.0, tk.END)
        
        if not stock_data:
            self.stock_data_text.insert(tk.END, "Stock data unavailable.\n")
            self.stock_data_text.config(state=tk.DISABLED)
            return
        
        # Format stock data display
        current = stock_data.get('c', 0)
        change = stock_data.get('d', 0)
        change_pct = stock_data.get('dp', 0)
        change_symbol = "+" if change >= 0 else ""
        
        display_text = f"Ticker: {self.ticker}\n"
        display_text += f"{'=' * 50}\n\n"
        display_text += f"Current Price:        ${current:>10,.2f}\n"
        display_text += f"Previous Close:      ${stock_data.get('pc', 0):>10,.2f}\n"
        display_text += f"Change:              {change_symbol}${change:>9,.2f} ({change_pct:>5.2f}%)\n"
        display_text += f"\n{'-' * 50}\n\n"
        display_text += f"High (Today):        ${stock_data.get('h', 0):>10,.2f}\n"
        display_text += f"Low (Today):         ${stock_data.get('l', 0):>10,.2f}\n"
        display_text += f"Open (Today):        ${stock_data.get('o', 0):>10,.2f}\n"
        
        # Color code the change
        self.stock_data_text.insert(tk.END, display_text)
        
        # Apply color to change line
        change_start = display_text.find("Change:")
        if change_start != -1:
            if change >= 0:
                color = self.colors['positive']
            else:
                color = self.colors['negative']
            # Tag the change line (simplified - in production, use tags for line-specific coloring)
        
        self.stock_data_text.config(state=tk.DISABLED)
    
    def _display_sentiment_summary(self, overall_label: str, overall_score: float, sentiment_scores: List[float]):
        """Display overall sentiment summary."""
        self.sentiment_summary_text.config(state=tk.NORMAL)
        self.sentiment_summary_text.delete(1.0, tk.END)
        
        positive_count = sum(1 for s in sentiment_scores if s > 0)
        negative_count = sum(1 for s in sentiment_scores if s < 0)
        neutral_count = sum(1 for s in sentiment_scores if s == 0)
        total = len(sentiment_scores)
        
        # Determine color based on sentiment
        if overall_label == "POSITIVE":
            color = self.colors['positive']
        elif overall_label == "NEGATIVE":
            color = self.colors['negative']
        else:
            color = self.colors['neutral']
        
        summary_text = f"Overall Sentiment: {overall_label}\n"
        summary_text += f"Average Score: {overall_score:.4f}\n\n"
        summary_text += f"Total Articles Analyzed: {total}\n\n"
        summary_text += f"Sentiment Breakdown:\n"
        summary_text += f"  - Positive: {positive_count} ({positive_count*100//total if total > 0 else 0}%)\n"
        summary_text += f"  - Negative: {negative_count} ({negative_count*100//total if total > 0 else 0}%)\n"
        summary_text += f"  - Neutral: {neutral_count} ({neutral_count*100//total if total > 0 else 0}%)\n"
        
        self.sentiment_summary_text.insert(tk.END, summary_text)
        self.sentiment_summary_text.config(state=tk.DISABLED)
        
        # Update distribution visualization
        self._display_distribution(positive_count, negative_count, neutral_count, total)
    
    def _display_distribution(self, positive: int, negative: int, neutral: int, total: int):
        """Display sentiment distribution with visual bars."""
        self.distribution_text.config(state=tk.NORMAL)
        self.distribution_text.delete(1.0, tk.END)
        
        if total == 0:
            self.distribution_text.insert(tk.END, "No data available.")
            self.distribution_text.config(state=tk.DISABLED)
            return
        
        max_count = max(positive, negative, neutral, 1)
        bar_length = 30
        
        pos_bar = "#" * int((positive / max_count) * bar_length)
        neg_bar = "#" * int((negative / max_count) * bar_length)
        neu_bar = "#" * int((neutral / max_count) * bar_length)
        
        # Pad bars
        pos_bar = pos_bar.ljust(bar_length)
        neg_bar = neg_bar.ljust(bar_length)
        neu_bar = neu_bar.ljust(bar_length)
        
        dist_text = f"Sentiment Distribution:\n\n"
        dist_text += f"Positive ({positive:>3}): [{pos_bar}] {positive*100//total:>3}%\n"
        dist_text += f"Negative ({negative:>3}): [{neg_bar}] {negative*100//total:>3}%\n"
        dist_text += f"Neutral  ({neutral:>3}): [{neu_bar}] {neutral*100//total:>3}%\n"
        
        self.distribution_text.insert(tk.END, dist_text)
        self.distribution_text.config(state=tk.DISABLED)
    
    def _display_articles(self, articles: List[Dict]):
        """Display articles in the listbox."""
        self.articles_listbox.delete(0, tk.END)
        
        for i, article in enumerate(articles, 1):
            title = article['title'][:80] + "..." if len(article['title']) > 80 else article['title']
            label = article['sentiment_label']
            score = article['sentiment_score']
            
            # Format with sentiment indicator
            display_text = f"[{i:>3}] [{label[:3]}] {title}"
            self.articles_listbox.insert(tk.END, display_text)
            
            # Color code based on sentiment
            if label == "POSITIVE":
                self.articles_listbox.itemconfig(tk.END - 1, {'fg': self.colors['positive']})
            elif label == "NEGATIVE":
                self.articles_listbox.itemconfig(tk.END - 1, {'fg': self.colors['negative']})
            else:
                self.articles_listbox.itemconfig(tk.END - 1, {'fg': self.colors['neutral']})
    
    def _display_top_articles(self, articles: List[Dict]):
        """Display top positive and negative articles."""
        # Sort articles by sentiment score
        sorted_articles = sorted(articles, key=lambda x: x['sentiment_score'], reverse=True)
        
        # Top positive (highest scores)
        self.top_positive_listbox.delete(0, tk.END)
        positive_articles = [a for a in sorted_articles if a['sentiment_score'] > 0]
        for article in positive_articles[:10]:  # Top 10
            title = article['title'][:60] + "..." if len(article['title']) > 60 else article['title']
            score = article['sentiment_score']
            self.top_positive_listbox.insert(tk.END, f"[{score:+.3f}] {title}")
        
        # Top negative (lowest scores)
        self.top_negative_listbox.delete(0, tk.END)
        negative_articles = [a for a in sorted_articles if a['sentiment_score'] < 0]
        for article in negative_articles[:10]:  # Top 10
            title = article['title'][:60] + "..." if len(article['title']) > 60 else article['title']
            score = article['sentiment_score']
            self.top_negative_listbox.insert(tk.END, f"[{score:+.3f}] {title}")
    
    def _on_article_select(self, event):
        """Handle article selection event."""
        selection = self.articles_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if self.current_results and index < len(self.current_results['articles']):
            article = self.current_results['articles'][index]
            
            # Display article details
            self.article_details_text.config(state=tk.NORMAL)
            self.article_details_text.delete(1.0, tk.END)
            
            details = f"Title: {article['title']}\n\n"
            details += f"Published: {article['published']}\n\n"
            details += f"Sentiment: {article['sentiment_label']}\n"
            details += f"Score: {article['sentiment_score']:.4f}\n\n"
            details += f"Link: {article['link']}\n\n"
            details += f"Summary:\n{article.get('summary', 'No summary available.')}\n"
            
            self.article_details_text.insert(tk.END, details)
            
            # Color code sentiment
            if article['sentiment_label'] == "POSITIVE":
                color = self.colors['positive']
            elif article['sentiment_label'] == "NEGATIVE":
                color = self.colors['negative']
            else:
                color = self.colors['neutral']
            
            # Apply color to sentiment line (simplified - tags would be better)
            self.article_details_text.config(state=tk.DISABLED)
    
    def _update_recommendation(self, stock_data: Optional[Dict], sentiment_score: float):
        """Calculate and display investment recommendation."""
        if not stock_data:
            self.recommendation_label.config(text="N/A - No stock data", fg=self.colors['text_light'])
            return
        
        # Get stock trend (positive if price increased)
        change_pct = stock_data.get('dp', 0)  # Daily change percentage
        
        # Combine sentiment and stock trend for recommendation
        # BUY: Positive sentiment AND positive trend
        # SELL: Negative sentiment AND negative trend
        # HOLD: Everything else
        
        if sentiment_score > SENTIMENT_THRESHOLD_POSITIVE and change_pct > 0:
            recommendation = "[BUY]"
            color = self.colors['positive']
        elif sentiment_score < SENTIMENT_THRESHOLD_NEGATIVE and change_pct < 0:
            recommendation = "[SELL]"
            color = self.colors['negative']
        else:
            recommendation = "[HOLD]"
            color = self.colors['neutral']
        
        self.recommendation_label.config(text=f"Recommendation: {recommendation}", fg=color)
    
    def export_to_json(self):
        """Export current results to JSON file."""
        if not self.current_results:
            messagebox.showwarning("Warning", "No data to export. Please refresh data first.")
            return
        
        # Ask user for file location
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_results, f, indent=2, default=str)
                messagebox.showinfo("Success", f"Results exported to:\n{filename}")
                self._update_status(f"Exported to: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{str(e)}")


def check_display_available():
    """
    Check if a display is available for GUI applications.
    
    Returns:
        bool: True if display is available, False otherwise
    """
    import os
    display = os.environ.get('DISPLAY')
    
    # Check if DISPLAY is set
    if not display:
        return False
    
    # Try to import tkinter and create a test window
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the test window
        root.destroy()
        return True
    except Exception:
        return False


def main():
    """Main entry point for the GUI application."""
    import os
    import sys
    
    # Check if display is available
    if not os.environ.get('DISPLAY'):
        print("=" * 70)
        print("ERROR: No display available for GUI application")
        print("=" * 70)
        print("\nThis GUI application requires a display server (X11) to run.")
        print("\nSOLUTIONS:")
        print("\n1. If you're on a remote server:")
        print("   - Use X11 forwarding: ssh -X user@server")
        print("   - Or use VNC/Xvfb virtual display")
        print("\n2. Install Xvfb for headless environments:")
        print("   sudo apt-get install xvfb")
        print("   xvfb-run -a python gui_app.py")
        print("\n3. Use Docker with X11 forwarding:")
        print("   docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ...")
        print("\n4. Use the CLI version instead:")
        print("   python main.py")
        print("\n5. For WSL (Windows Subsystem for Linux):")
        print("   - Install an X server (VcXsrv, X410, etc.)")
        print("   - Set DISPLAY=localhost:0.0")
        print("\nFor more information, see GUI_USAGE.md")
        print("=" * 70)
        sys.exit(1)
    
    # Try to create the main window
    try:
        root = tk.Tk()
        app = StockSentimentGUI(root)
        root.mainloop()
    except tk.TclError as e:
        if "no display name" in str(e) or "$DISPLAY" in str(e):
            print("=" * 70)
            print("ERROR: Cannot connect to display")
            print("=" * 70)
            print(f"\nError details: {e}")
            print("\nPlease ensure:")
            print("  1. DISPLAY environment variable is set correctly")
            print("  2. X server is running and accessible")
            print("  3. X11 forwarding is enabled (for SSH connections)")
            print("\nAlternatively, use the CLI version: python main.py")
            print("=" * 70)
            sys.exit(1)
        else:
            raise


if __name__ == "__main__":
    main()
