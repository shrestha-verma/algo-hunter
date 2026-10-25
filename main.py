import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from database import init_db, get_or_create_user, save_problem_record, get_user_history, get_all_users
from agent import analyze_dsa_code

load_dotenv()

app = FastAPI(title="Algo Hunter API", version="2.0.0")

class AnalyzeRequest(BaseModel):
    username: str = "shrestha"
    code_snippet: str
    problem_context: str = ""

class LoginRequest(BaseModel):
    username: str

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/users/all")
def fetch_users():
    return {"users": get_all_users()}

@app.post("/user/login")
def login_user(req: LoginRequest):
    if not req.username or not req.username.strip():
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    user = get_or_create_user(req.username)
    return {"status": "ok", "username": user}

@app.get("/user/{username}/history")
def fetch_user_history(username: str):
    clean_user = username.strip().lower()
    history = get_user_history(clean_user)
    return {"username": clean_user, "history": history}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    if not req.code_snippet or len(req.code_snippet.strip()) < 5:
        raise HTTPException(status_code=400, detail="Code snippet too short.")
    
    clean_user = get_or_create_user(req.username)
    
    # Pure agentic execution via Nemotron on Nebius
    result = analyze_dsa_code(req.code_snippet, req.problem_context)
    
    if "error" in result:
        return result
        
    # Save persistent record to SQLite
    save_problem_record(clean_user, result, req.code_snippet, req.problem_context)
    return result

# Serve static frontend files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)