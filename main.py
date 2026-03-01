from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# We need to tell litellm that we are using groq. 
os.environ["OPENAI_API_KEY"] = "dummy_key"
os.environ["MODEL_NAME"] = "groq/llama-3.3-70b-versatile"

# Import our CrewAI Orchestrator
from agents.crew_orchestrator import ProductivityCrew

app = FastAPI(
    title="Multi-Agent Personal Productivity Ecosystem",
    description="API for interacting with the CrewAI productivity agents."
)

# Initialize the Crew
try:
    crew = ProductivityCrew()
except Exception as e:
    print(f"Warning: Failed to initialize Crew. Ensure API keys are set. Error: {e}")
    crew = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Multi-Agent Personal Productivity Ecosystem API is running."}

@app.post("/chat", response_model=ChatResponse)
def chat_with_agents(request: ChatRequest):
    if not crew:
        raise HTTPException(status_code=500, detail="Crew orchestration not initialized. Check API keys.")
    
    try:
        # Pass the user's message to the Crew
        result = crew.process_request(request.message)
        return ChatResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Allow running directly via python main.py
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
