from os import getenv
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

MODEL = "gpt-4o"