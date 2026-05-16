from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI(title="PIXORA AI API")

# CORS (App + Website connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")


# Request body
class ChatRequest(BaseModel):
    message: str


# Home route
@app.get("/")
def home():
    return {
        "status": "online",
        "name": "PIXORA-AI-3",
        "message": "PIXORA AI API Running"
    }


# Chat route
@app.post("/chat")
def chat(data: ChatRequest):
    try:
        response = model.generate_content(data.message)

        return {
            "success": True,
            "reply": response.text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
