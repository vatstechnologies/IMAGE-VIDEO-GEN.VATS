import openai
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, concatenate_videoclips
from config import OPENAI_API_KEY, ELEVEN_LABS_API_KEY, HYGEN_API_KEY
import streamlit as st

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Streamlit interface
st.title('VatsGenixAI - AI Podcast Generator')

# Text input for Podcast topic
topic = st.text_input("Enter Podcast Topic:")

# Generate text based on input topic using OpenAI GPT
if topic:
    st.subheader("Generating Podcast Script...")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate a podcast script on {topic}",
        max_tokens=1500
    )
    script = response.choices[0].text.strip()
    st.write(script)

    # Convert script to speech using Eleven Labs or gTTS
    speech_option = st.selectbox("Choose Speech Engine:", ["gTTS", "Eleven Labs"])
    
    if speech_option == "gTTS":
        st.subheader("Generating Podcast Audio (gTTS)...")
        tts = gTTS(text=script, lang='en')
        tts.save("podcast.mp3")
        st.audio("podcast.mp3")
    elif speech_option == "Eleven Labs":
        st.subheader("Generating Podcast Audio (Eleven Labs)...")
        audio_url = "https://api.elevenlabs.io/v1/synthesize"  # Example URL, adjust accordingly
        headers = {"Authorization": f"Bearer {ELEVEN_LABS_API_KEY}"}
        data = {"text": script, "voice": "en_us_male"}
        response = requests.post(audio_url, headers=headers, json=data)
        
        if response.status_code == 200:
            audio_file = response.content
            with open("podcast_elevenlabs.mp3", "wb") as f:
                f.write(audio_file)
            st.audio("podcast_elevenlabs.mp3")
        else:
            st.error("Error generating podcast audio with Eleven Labs.")

    # Generate a visual representation (image or video)
    if st.checkbox("Generate Podcast Video"):
        st.subheader("Creating Podcast Video...")

        # Example: Create a video with static image (You can modify this to suit your needs)
        image_clip = ImageClip("background_image.jpg").set_duration(10)
        audio_clip = "podcast.mp3"  # Use generated audio file
        video = image_clip.set_audio(audio_clip)
        video.write_videofile("podcast_video.mp4", fps=24)

        st.video("podcast_video.mp4")
