# GUI Application Usage Guide

## Quick Start

To launch the graphical desktop application:

```bash
python gui_app.py
```

The application will:
- Open automatically when you run the script
- Load your configuration from `.env` file
- Start fetching data automatically after a brief delay

## Features

### ?? Summary & Stock Data Tab
- **Real-Time Stock Data**: Displays current price, daily change, high/low/open prices
- **Overall Sentiment Analysis**: Shows total articles analyzed, average sentiment score, and overall classification
- **Sentiment Distribution**: Visual bars showing positive/negative/neutral article distribution

### ?? News Articles Tab
- **Latest News Articles**: Scrollable list of all analyzed articles with sentiment indicators
- **Article Details**: Click any article to see full details (title, date, link, summary, sentiment score)
- **Top Positive Articles**: List of articles with highest positive sentiment scores
- **Top Negative Articles**: List of articles with lowest (most negative) sentiment scores

### ?? Investment Recommendation
- **Real-time Recommendation**: Displayed in the header
  - **[BUY]**: Positive sentiment + positive stock trend
  - **[SELL]**: Negative sentiment + negative stock trend  
  - **[HOLD]**: All other scenarios

### ?? Controls
- **Refresh Data Button**: Fetches latest stock data and news articles, then performs fresh sentiment analysis
- **Export to JSON Button**: Saves current analysis results to a JSON file (prompts for file location)

### ?? Progress Tracking
- Status bar at the bottom shows current operation
- Progress indicator shows analysis progress
- Color-coded sentiment (Green=Positive, Red=Negative, Yellow=Neutral)

## Requirements

Same as the CLI version:
- Python 3.8+
- All dependencies from `requirements.txt`
- Configured `.env` file with `API_KEY`, `TICKER`, and `KEYWORD`

## Notes

- The GUI runs analysis in background threads to keep the interface responsive
- Initial data loading may take 30-60 seconds depending on number of articles
- Console output from underlying classes may appear but doesn't affect GUI functionality
- The application auto-loads data on startup (after 0.5 seconds delay)

## Troubleshooting

### Display/Display Server Issues

**Error: "no display name and no $DISPLAY environment variable"**

This means you're running in a headless environment (no GUI display available). Solutions:

#### Option 1: Use Xvfb (Virtual Display) - Recommended for Servers
```bash
# Install Xvfb
sudo apt-get update
sudo apt-get install xvfb

# Run GUI with virtual display
xvfb-run -a python gui_app.py
```

#### Option 2: Use X11 Forwarding (SSH)
```bash
# Connect with X11 forwarding enabled
ssh -X user@server

# Then run normally
python gui_app.py
```

#### Option 3: Docker with X11
```bash
docker run -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/workspace \
  your-image python gui_app.py
```

#### Option 4: WSL (Windows Subsystem for Linux)
1. Install an X server (VcXsrv, X410, or MobaXterm)
2. Start the X server
3. Set display:
   ```bash
   export DISPLAY=localhost:0.0
   python gui_app.py
   ```

#### Option 5: Use CLI Version Instead
If you don't need the GUI, use the command-line version:
```bash
python main.py
```

### Other Issues

**Application won't start:**
- Check that your `.env` file is properly configured
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that Python 3.8+ is installed

**No data showing:**
- Click "Refresh Data" button
- Check your internet connection
- Verify API key is valid in `.env` file

**Slow performance:**
- Analysis runs in background - wait for progress indicator to complete
- First run takes longer as AI model loads into memory
