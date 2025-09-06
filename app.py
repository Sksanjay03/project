from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from main import analyze_resume
import os
import uuid
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze-resume/")
async def analyze_resume_api(
    file: UploadFile = File(...),
    interest: str = Form("General")
):
    # Save uploaded file to a local path
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Analyze the uploaded resume
    result = analyze_resume(file_path, user_interest=interest)

    if not result:
        return JSONResponse(status_code=500, content={"error": "Resume processing failed"})

    return {
        "resume_path": file_path,
        "interest": interest,
        **result
    }
