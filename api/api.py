from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from os import getenv
from dotenv import load_dotenv

from config.prompts import SYSTEM_PROMPT
from config.llm_config import MODEL
from analyze import analyze

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ConversationRequest(BaseModel):
    messages: list[Message]

# Takes a conversation and returns sentiment analysis
@app.post("/analyze/")
async def analyze_sentiment(request: ConversationRequest):
    try:
        return analyze(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))