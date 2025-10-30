# Setup Guide - Fixing API Key Error

## Problem
If you're seeing: `Error: Missing or invalid environment variables: API_KEY`

This means your `.env` file still has placeholder text instead of your actual API key.

## Quick Fix Steps

### 1. Open your `.env` file
The file is located at: `/workspaces/AI-NLP-Analysis-and-Stock-Data-Script/.env`

### 2. Replace the placeholder API key

**Current (WRONG):**
```
API_KEY=your_finnhub_api_key_here
```

**Should be (CORRECT):**
```
API_KEY=your_actual_api_key_from_finnhub
```

### 3. Important Formatting Rules

? **Correct format:**
```
API_KEY=abc123xyz456
TICKER=META
KEYWORD=Meta Platforms
```

? **Wrong formats:**
```
API_KEY = abc123xyz456    (spaces around =)
API_KEY= abc123xyz456     (space after =)
API_KEY=abc123xyz456      (this is fine, but make sure no trailing spaces)
API_KEY="abc123xyz456"    (quotes not needed)
```

### 4. Common Issues

**Issue 1: Spaces around equals sign**
- Wrong: `API_KEY = abc123`
- Right: `API_KEY=abc123`

**Issue 2: Using placeholder text**
- Wrong: `API_KEY=your_finnhub_api_key_here`
- Right: `API_KEY=c123abc456def789`

**Issue 3: Empty value**
- Wrong: `API_KEY=`
- Right: `API_KEY=your_actual_key`

**Issue 4: Comment on same line**
- Wrong: `API_KEY=abc123  # my key`
- Right: Put comments on separate lines or use `#` at the start

### 5. Verify Your Setup

After editing your `.env` file, run:
```bash
python main.py
```

The debug output will show what values were detected. If you still see an error, check:
- Did you save the file?
- Are there any spaces around the `=` sign?
- Did you use your actual API key (not the placeholder)?
- Is the API key on one line without quotes?

### 6. Get Your Finnhub API Key

If you don't have an API key yet:
1. Go to https://finnhub.io/register
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Paste it into your `.env` file

### 7. Testing Your Configuration

You can test if your .env file is configured correctly:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API_KEY loaded:', 'YES' if os.getenv('API_KEY') and not os.getenv('API_KEY').startswith('your_') else 'NO')"
```

This should print `API_KEY loaded: YES` if configured correctly.

## Still Having Issues?

If you're still getting errors after following these steps:

1. **Check file location**: Make sure you're editing `.env` in the project root directory
2. **Check file name**: The file must be named exactly `.env` (with the dot at the start)
3. **Check encoding**: Make sure the file is saved as plain text (UTF-8)
4. **Restart**: Try closing and reopening your editor/terminal
5. **Check hidden characters**: Make sure there are no invisible characters or special formatting

## Example .env File

Here's what a properly configured `.env` file should look like:

```
# Finnhub API Configuration
API_KEY=c123abc456def789ghi012jkl345mno678pqr901stu234vwx567yz

# Stock ticker symbol
TICKER=META

# News search keyword
KEYWORD=Meta Platforms
```

Notice:
- No spaces around `=`
- Real API key (not placeholder)
- Comments are on separate lines
- Each variable on its own line
