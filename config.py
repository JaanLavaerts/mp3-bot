import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
GIPHY_API_KEY = os.getenv('GIPHY')