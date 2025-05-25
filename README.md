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
*   🔗 **LinkedIn Integration:** Authorize the app to connect to your LinkedIn account.
*   📝 **Auto-Post to Feed:** Directly post the generated knowledge summary to your LinkedIn feed (visible to your connections).
*   🔒 **Secure OAuth 2.0:** Uses OAuth 2.0 for LinkedIn authentication, ensuring your credentials are not directly handled by the app.
*   👤 **Login Status:** Shows your current LinkedIn login status and user name.

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
LINKEDIN_CLIENT_ID = "YOUR_LINKEDIN_CLIENT_ID_HERE"
LINKEDIN_CLIENT_SECRET = "YOUR_LINKEDIN_CLIENT_SECRET_HERE"
LINKEDIN_REDIRECT_URI = "YOUR_STREAMLIT_APP_URL_HERE" # e.g., http://localhost:8501 or your Streamlit Cloud URL
```

**⚠️ Important:**
*   Replace the placeholder values with your *actual* API keys.
*   Get a YouTube Data API key from the [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com).
*   Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
*   `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, and `LINKEDIN_REDIRECT_URI` are required for the LinkedIn OAuth integration.
    *   Obtain `CLIENT_ID` and `CLIENT_SECRET` by creating an app on the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps/new).
    *   Set `LINKEDIN_REDIRECT_URI` to the URL of your Streamlit application (e.g., `http://localhost:8501` for local development, or your actual Streamlit Cloud URL if deployed).
    *   **Crucially, this exact `LINKEDIN_REDIRECT_URI` value must also be added to your LinkedIn Developer App's configuration under "Authorized redirect URLs".**

### 4.1. LinkedIn App Setup Details

To use the LinkedIn integration, you need to create an app on the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps/new).

During app creation or configuration:
1.  **App Information:** Fill in the required details like app name, company, and logo.
2.  **Products:** After creating the app, you will need to add "Products" to it. Request the following products:
    *   `Sign In with LinkedIn using OpenID Connect` (provides `openid` and `profile` scopes)
    *   `Share on LinkedIn` (provides `w_member_social` scope for posting)
    You might need to wait for approval from LinkedIn for these products.
3.  **Authentication Tab:**
    *   Note down your `Client ID` (this is your `LINKEDIN_CLIENT_ID`) and `Client Secret` (this is your `LINKEDIN_CLIENT_SECRET`).
    *   Under **OAuth 2.0 settings**:
        *   Click "+ Add redirect URL" to add your `LINKEDIN_REDIRECT_URI`. This **must exactly match** the value in your `secrets.toml`.
            *   For local development, this is typically `http://localhost:8501`.
            *   If deploying to Streamlit Community Cloud, this will be your app's URL (e.g., `https://your-app-name.streamlit.app/`). You can add multiple redirect URIs if needed (e.g., one for local, one for deployed).
4.  **Verification (Optional but Recommended):**
    * Some LinkedIn Developer features may require app verification. Follow LinkedIn's instructions if prompted.

*   **Never commit your `secrets.toml` file!** The included `.gitignore` file should already prevent this.

---

## ▶️ How to Run

With setup complete, launch the Streamlit app from your terminal:

```bash
streamlit run linkedin_streamlit_app.py
```

Your browser should automatically open the application.

### Application Workflow:
1.  **(Optional but Recommended) Login with LinkedIn:**
    *   Click the "Login with LinkedIn" button at the top of the page.
    *   You will be redirected to LinkedIn to authorize the application.
    *   Upon successful authorization, you will be redirected back to the app, and it will display your LinkedIn name.
2.  **Generate Knowledge Post:**
    *   Enter a YouTube video URL into the input field.
    *   Click "Generate Knowledge Post".
    *   The app will fetch video details, get the transcript, and use Gemini AI to create a LinkedIn post draft.
3.  **Post to LinkedIn:**
    *   If you are logged into LinkedIn and the post has been generated, a "🚀 Post to LinkedIn" button will appear.
    *   Click this button to share the generated content directly to your LinkedIn feed (it will be visible to your connections).
    *   You'll receive a confirmation message upon successful posting.
