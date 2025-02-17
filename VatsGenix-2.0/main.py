import streamlit as st
import openai
import os
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import pyttsx3

# Load environment variables from .env
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Hugging Face API Key (Optional)
HYGEN_API_KEY = os.getenv("HYGEN_API_KEY")

# 11 Labs API Key (Optional for Text-to-Speech)
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# Streamlit App Title
st.title("🖼️✨ VatsGenix.AI - AI Image & Text Generator")

# Sidebar for Navigation
st.sidebar.title("🔍 Select Mode")
option = st.sidebar.radio("Choose an AI Task:", ["Generate Text", "Generate Image", "Text-to-Speech"])

### ========================== TEXT GENERATION ============================
if option == "Generate Text":
    st.subheader("📝 AI-Powered Text Generation")
    user_input = st.text_area("Enter your prompt:", "Write a futuristic story about AI.")

    if st.button("Generate Text"):
        if user_input:
            with st.spinner("Generating text..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful AI assistant."},
                            {"role": "user", "content": user_input}
                        ],
                        max_tokens=200
                    )
                    generated_text = response['choices'][0]['message']['content']
                    st.success("✅ Successfully generated!")
                    st.write(generated_text)
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

### ========================== IMAGE GENERATION ============================
elif option == "Generate Image":
    st.subheader("🖼️ AI-Powered Image Generation")
    img_prompt = st.text_area("Enter an image description:", "A futuristic cyberpunk city at night.")

    if st.button("Generate Image"):
        if img_prompt:
            with st.spinner("Generating image..."):
                try:
                   response = openai.images.generate(
    model="dall-e-3",
    prompt=img_prompt,
    size="1024x1024",
    quality="standard",
    n=1
)
image_url = response.data[0].url

                    st.image(image_url, caption="Generated Image")
                    st.success("✅ Successfully generated!")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

### ========================== TEXT-TO-SPEECH (11 LABS) ============================
elif option == "Text-to-Speech":
    st.subheader("🔊 AI-Powered Text-to-Speech")
    tts_text = st.text_area("Enter text to convert into speech:", "Hello, this is an AI-generated voice.")

    if st.button("Convert to Speech"):
        if tts_text:
            with st.spinner("Converting to speech..."):
                try:
                    response = requests.post(
                        "https://api.elevenlabs.io/v1/text-to-speech",
                        json={"text": tts_text},
                        headers={"Authorization": f"Bearer {ELEVEN_LABS_API_KEY}"}
                    )
                    audio_data = response.content
                    st.audio(audio_data, format="audio/mp3")
                    st.success("✅ Successfully generated speech!")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

# Footer
st.markdown("🚀 Developed by **VatsGenix AI**")
