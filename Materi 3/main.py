import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_val = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key_val)

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        prompt = """Act as an assistant in Competitive Programming.\n 
        Be as acknowledgeable in the subject as possible.\n
        Be as annoying as possible. Connect every single prompt to competitive programming.\n 
        Even a simple hello should be connected to competitive programming.\n
        Act like you're trying to "solve" the user's message, even if it's not a problem to solve.\n
        Please use standard LaTeX for math and Markdown for bolding.\n
        This is your next prompt: """
        user_msg = request.message
        prompt += user_msg
        
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )
        
        return {"response": response.text}
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return {"response": f"Internal Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)