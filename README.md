# LinkedIn Knowledge Post Generator (from YouTube Video)

This Streamlit application helps you generate engaging LinkedIn posts summarizing key takeaways from YouTube videos. It uses the YouTube Data API to fetch video details, the `youtube-transcript-api` to get the transcript, and Google's Gemini AI to craft a knowledge-sharing post **without including the original YouTube link**.

## Features

*   Accepts a YouTube video URL as input.
*   Fetches video title and description via YouTube API.
*   Retrieves the video transcript (if available).
*   Uses Google Gemini AI to analyze the content (title, description, transcript) and generate a LinkedIn post focused on key insights and takeaways.
*   The generated post is designed for knowledge sharing and does **not** contain the source YouTube link.
*   Includes a fallback mechanism for manual input if YouTube API calls fail.
*   Simple Streamlit interface for ease of use.

## Setup

### 1. Clone the Repository (if applicable)

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

The required packages are listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```

### 4. Configure Streamlit Secrets

This application requires API keys for YouTube and Google Gemini. You need to configure these using Streamlit Secrets.

Create a file named `.streamlit/secrets.toml` in your project directory (create the `.streamlit` folder if it doesn't exist). Add your API keys to this file:

```toml
# .streamlit/secrets.toml

YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

**Important:**
*   Replace `"YOUR_YOUTUBE_API_KEY_HERE"` with your actual YouTube Data API v3 key.
*   Replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual Google AI (Gemini) API key.
*   **Never commit your `secrets.toml` file to version control.** Add `.streamlit/secrets.toml` to your `.gitignore` file.

## How to Run

Once the dependencies are installed and secrets are configured, run the Streamlit application from your terminal:

```bash
streamlit run linkedin_streamlit_app.py
```

This will open the application in your default web browser. Enter a YouTube video URL and click "Generate Knowledge Post" to get your LinkedIn content.
