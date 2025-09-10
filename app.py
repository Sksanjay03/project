from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import shutil

from main import analyze_resume

app = FastAPI(title="Phi Resume Analyzer")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

latest_result = {}

@app.get("/")
def read_root():
    if latest_result:
        return latest_result
    return {"message": "Upload a resume at /analyze-resume/ to get started."}

@app.post("/analyze-resume/")
async def analyze_resume_api(
    file: UploadFile = File(...),
    interest: str = Form("General")
):
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_resume(file_path, user_interest=interest)

    if not result:
        return JSONResponse(status_code=500, content={"error": "Resume processing failed"})

    global latest_result
    latest_result = {
        "resume_path": file_path,
        "interest": interest,
        "agent_output": result
    }

    return latest_result
