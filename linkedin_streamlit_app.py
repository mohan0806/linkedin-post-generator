import streamlit as st
import re
from urllib.parse import urlparse, parse_qs
import googleapiclient.discovery
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# --- API Keys (Replace with your actual API keys or use Streamlit secrets) ---
YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY") # Use Streamlit secrets for API keys
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") # Use Streamlit secrets for API keys

if not YOUTUBE_API_KEY or not GEMINI_API_KEY:
    st.error("Please set your YouTube API key and Gemini API key in Streamlit secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
generation_config = genai.GenerationConfig(
    temperature=0.7,
    top_p=0.8,
    top_k=40,
    candidate_count=1,
    max_output_tokens=800, # Increased max tokens to handle transcript context
)
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]
gemini_model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp",
                                     generation_config=generation_config,
                                     safety_settings=safety_settings)


def is_valid_youtube_url(url):
    """Checks if the given URL is a valid YouTube video URL."""
    parsed_url = urlparse(url)
    if parsed_url.netloc in ('www.youtube.com', 'youtube.com', 'youtu.be'):
        if parsed_url.netloc in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                query_params = parse_qs(parsed_url.query)
                if 'v' in query_params:
                    return True
        elif parsed_url.netloc == 'youtu.be':
            if parsed_url.path:  # Should have a path (video ID)
                return True
    return False

def get_youtube_video_details(video_id):
    """
    Retrieves video title and description from YouTube API.
    """
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if response and 'items' in response and response['items']:
            item = response['items'][0]
            title = item['snippet']['title']
            description = item['snippet']['description']
            return title, description
        else:
            return None, None # Video not found or error
    except Exception as e:
        st.error(f"Error fetching YouTube video details: {e}")
        return None, None

def get_youtube_transcript(video_id):
    """
    Retrieves the transcript of a YouTube video.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Format transcript into a single string
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except TranscriptsDisabled:
        st.warning("Transcripts are disabled for this YouTube video.")
        return None
    except NoTranscriptFound:
        st.warning("No transcript found for this YouTube video (or not in English).")
        return None
    except Exception as e:
        st.error(f"Error fetching YouTube transcript: {e}")
        return None


def create_linkedin_post_with_gemini(video_title, video_description, transcript=None): # Removed youtube_link
    """
    Generates a LinkedIn post using Gemini API, incorporating video details and transcript,
    for knowledge sharing, WITHOUT including the YouTube link.
    """

    prompt_text = f"""
    Create a **catchy and engaging** LinkedIn post to share knowledge and key takeaways
    inspired by a YouTube video I recently watched.

    Video Title: {video_title}
    Video Description: {video_description}

    """
    if transcript:
        prompt_text += f"""
    Video Transcript (for context -  use this to understand the video's content in detail and extract key learnings):
    {transcript}

    Identify the most valuable insights, key concepts, and actionable advice from the video and transcript.
    Craft a LinkedIn post that shares this knowledge in your own words, as if you are sharing your learnings with your network.
    Focus on providing value and sparking discussion among your LinkedIn connections.
    Do NOT mention that this is from a YouTube video and DO NOT include any YouTube link in the post.

    **Structure the LinkedIn post for readability and impact.**
    - **Use bullet points or numbered lists to highlight key takeaways** if appropriate and if they emerge naturally from the content.
    - **Incorporate bold and *italic* text to emphasize important phrases and keywords.**
    - **Use relevant emojis** to make the post visually appealing and engaging.
    """

    prompt_text += """
    The LinkedIn post should be:
    - Thought-provoking and valuable to a professional audience.
    - Clearly articulate the key takeaways or insights, **ideally in point form if feasible**.
    - Encourage engagement and discussion in the comments.
    - Include relevant professional hashtags (e.g., #leadership, #innovation, #technology, #career, #learning, etc.).
    - Use emojis to make it visually appealing and engaging.
    - Aim for a length suitable for LinkedIn (around 3-4 short paragraphs).

    LinkedIn Post (WITHOUT YouTube Link):
    """

    try:
        response = gemini_model.generate_content(prompt_text)
        linkedin_post_text = response.text
        if linkedin_post_text:
            return linkedin_post_text
        else:
            return "Gemini API failed to generate a post. Gemini API failed to generate a post. Please try again or check your API key and prompt."

    except Exception as e:
        st.error(f"Error generating LinkedIn post with Gemini API: {e}")
        return "Error generating post. Please check your Gemini API key and connection."


def create_knowledge_linkedin_post_from_youtube(youtube_link): # Renamed function
    """
    Generates a LinkedIn post for sharing knowledge from a YouTube video, WITHOUT YouTube link in post.
    """

    if not is_valid_youtube_url(youtube_link):
        return "Invalid YouTube URL provided. Please provide a valid YouTube video link."

    video_id = None
    parsed_url = urlparse(youtube_link)
    if parsed_url.netloc in ('www.youtube.com', 'youtube.com'):
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v')[0]
    elif parsed_url.netloc == 'youtu.be':
        video_id = parsed_url.path[1:] # Remove leading '/'


    video_title, video_description = get_youtube_video_details(video_id)
    transcript_text = get_youtube_transcript(video_id) # Fetch transcript

    if not video_title or not video_description:
        st.warning("Could not fetch video title and description from YouTube API. Falling back to manual input.")
        manual_input = True
        return None # Signal to use manual input
    else:
        manual_input = False
        linkedin_post_text = create_linkedin_post_with_gemini(video_title, video_description, transcript_text) # Removed youtube_link from here
        return linkedin_post_text, manual_input


# --- Streamlit UI ---
st.title("💡 LinkedIn Knowledge Post Generator 🚀") # Updated Title
st.subheader("Share valuable insights from YouTube videos with your LinkedIn network!") # Updated Subheader

youtube_url_input = st.text_input("Enter YouTube Video Link (for analysis - URL will NOT be in the post):", placeholder="https://www.youtube.com/watch?v=...") # Updated Input Label

if st.button("Generate Knowledge Post"): # Updated Button Label
    if not youtube_url_input:
        st.error("Please enter a YouTube video link.")
    else:
        with st.spinner("Generating LinkedIn Knowledge Post with AI ... "): # Updated Spinner
            post_generation_result = create_knowledge_linkedin_post_from_youtube(youtube_url_input) # Updated function call

            if post_generation_result is None: # Manual input fallback
                st.session_state.manual_input_mode = True
                st.session_state.youtube_link_for_manual = youtube_url_input # Store link for manual mode
                st.experimental_rerun() # Rerun to show manual input fields

            else:
                linkedin_post_text, manual_input_used = post_generation_result
                if "Invalid YouTube URL" in linkedin_post_text or "Error generating" in linkedin_post_text or "Gemini API failed" in linkedin_post_text:
                    st.error(linkedin_post_text)
                else:
                    st.session_state.generated_post = linkedin_post_text
                    st.session_state.manual_input_mode = False # Reset manual input mode
                    st.success("LinkedIn Knowledge Post Generated Successfully (with better formatting!)") # Updated success message
                    st.balloons() # Celebrate!


if "manual_input_mode" in st.session_state and st.session_state.manual_input_mode:
    st.subheader("Manual Input Mode (YouTube API Failed)")
    st.write("We couldn't automatically fetch video details. Please provide them manually:")
    manual_video_title = st.text_input("Enter Video Title (for context):", placeholder="e.g., The Future of AI in Marketing") # Updated label
    manual_video_summary = st.text_area("Enter a Brief Summary (of the video):", placeholder="Summarize the video's main points...") # Updated label

    if st.button("Generate Post (Manual Input)"): # Button label remains
        if not manual_video_title or not manual_video_summary:
            st.error("Please enter both a title and a summary.")
        else:
            with st.spinner("Generating LinkedIn Post..."):
                linkedin_post_text_manual = create_linkedin_post_from_youtube(st.session_state.youtube_link_for_manual, video_title=manual_video_title, video_summary=manual_video_summary) # Using old fallback function

                if "Invalid YouTube URL" in linkedin_post_text_manual: # Should not happen here, but for safety
                    st.error(linkedin_post_text_manual)
                else:
                    st.session_state.generated_post = linkedin_post_text_manual
                    st.session_state.manual_input_mode = False # Reset manual input mode
                    st.success("LinkedIn Post Generated (Manual Input)!")
                    st.balloons()


if "generated_post" in st.session_state:
    st.subheader("Generated LinkedIn Knowledge Post:") # Updated Subheader
    st.markdown(st.session_state.generated_post) # Changed st.code to st.markdown

    st.markdown("---")
    st.markdown("💡 **Tips for LinkedIn:**")
    st.markdown("- Consider adding a relevant image to enhance your post.") # Updated tip
    st.markdown("- Tag relevant people or companies if applicable.")
    st.markdown("- Engage with comments and discussions to share more insights!") # Updated tip
    st.markdown("- Review and customize the post to perfectly reflect your knowledge and voice!") # Updated tip
    st.markdown("---")


# --- Helper function (old one, used for manual fallback) ---
def create_linkedin_post_from_youtube(youtube_link, video_title=None, video_summary=None):
    """
    Generates a LinkedIn post text from a YouTube link, prompting the user for details.
    Used as fallback when YouTube API fails.  This version still includes the YouTube link.
    """

    if not is_valid_youtube_url(youtube_link):
        return "Invalid YouTube URL provided. Please provide a valid YouTube video link."

    if video_title is None:
        video_title = "Insightful Learnings!" # Updated default title
    if video_summary is None:
        video_summary = "Key takeaways and reflections on a relevant topic." # Updated default summary


    key_takeaways_points = []
    # No user input for takeaways in fallback in this Streamlit version for simplicity, can be added if needed

    hashtags = ["#knowledge", "#insights", "#learning", "#linkedin", "#professionaldevelopment"] # Updated default hashtags
    # No hashtag input in fallback for simplicity, can be added

    call_to_action = "Let's discuss in the comments below!" # Updated default call to action
    # No call to action input in fallback

    # --- Construct the LinkedIn Post ---

    linkedin_post = f"📢 **Sharing some valuable insights I recently gained!** 📢\n\n" # Updated opening
    linkedin_post += f"🎬 **{video_title}** 🎬\n\n" # Keep title, but it's now more general
    linkedin_post += f"{video_summary}\n\n"

    if key_takeaways_points:
        linkedin_post += "🔑 **Key Takeaways:**\n"
        for point in key_takeaways_points:
            linkedin_post += f"👉 {point}\n"
        linkedin_post += "\n"

    # Removed YouTube link from here -  This fallback version now also does NOT include the YouTube link
    linkedin_post += f"➡️ {call_to_action} Share your thoughts and experiences! 👇\n\n" # Updated call to action

    if hashtags:
        linkedin_post += "#️⃣ " + " ".join(hashtags) + "\n\n"

    linkedin_post += "---\n#LinkedIn #KnowledgeSharing #ProfessionalGrowth #Insights" # Updated general hashtags

    return linkedin_post


# --- Run the Streamlit app ---
if __name__ == "__main__":
    pass # Keep this for clarity, no special main block needed for Streamlit