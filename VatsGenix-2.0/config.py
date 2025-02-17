import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')
HYGEN_API_KEY = os.getenv('HYGEN_API_KEY')
