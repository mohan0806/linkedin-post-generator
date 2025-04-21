# 🚀 LinkedIn Knowledge Post Generator (from YouTube Video) 💡

Transform YouTube video insights into engaging LinkedIn posts! This Streamlit app leverages the YouTube Data API, `youtube-transcript-api`, and Google's Gemini AI to generate knowledge-sharing content **without** including the original YouTube link.

---

## ✨ Features

*   📝 **YouTube URL Input:** Simply paste the video link.
*   🔍 **API Integration:** Fetches video title & description (YouTube API) and transcript (`youtube-transcript-api`).
*   🧠 **AI-Powered Content:** Uses Google Gemini to analyze video details and transcript, crafting a post focused on key takeaways.
*   🔗 **Link-Free Posts:** Generated content is designed for sharing *your* insights, not just linking the video.
*   🛠️ **Manual Fallback:** Provides an option for manual input if API calls encounter issues.
*   🖥️ **Simple UI:** Built with Streamlit for a clean and user-friendly experience.

---

## 🛠️ Setup Guide

Follow these steps to get the application running locally:

### 1. Clone the Repository

```bash
git clone https://github.com/mohan0806/linkedin-post-generator.git
cd linkedin-post-generator
```
*(Replace the URL if your repository location is different)*

### 2. Create & Activate Virtual Environment (Recommended)

```bash
# Create the environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies 📦

All required packages are listed in `requirements.txt`. Install them easily:

```bash
pip install -r requirements.txt
```

### 4. Configure Streamlit Secrets 🔑

The app needs API keys for YouTube and Google Gemini. Store them securely using Streamlit Secrets:

*   Create a directory named `.streamlit` in your project folder if it doesn't exist.
*   Inside `.streamlit`, create a file named `secrets.toml`.
*   Add your keys to `secrets.toml`:

```toml
# .streamlit/secrets.toml

YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

**⚠️ Important:**
*   Replace the placeholder values with your *actual* API keys.
*   Get a YouTube Data API key from the [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
*   Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
*   **Never commit your `secrets.toml` file!** The included `.gitignore` file should already prevent this.

---

## ▶️ How to Run

[Watch the Demo Video](Linkedin Post Generator.mp4) 🎬

With setup complete, launch the Streamlit app from your terminal:

```bash
streamlit run linkedin_streamlit_app.py
```

Your browser should automatically open the application. Paste a YouTube video URL, click "Generate Knowledge Post", and share your insights on LinkedIn!
