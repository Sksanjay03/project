from fastapi import FastAPI, UploadFile, File
import pdfplumber
import career_assistant  # use your local career_assistant.py module

app = FastAPI()

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    # Extract text from PDF
    with pdfplumber.open(file.file) as pdf:
        text = "\n".join([p.extract_text() or "" for p in pdf.pages])

    # Run through your custom pipeline
    parsed = career_assistant.resume_parser.run(
        f"Extract structured resume data:\n{text}"
    ).content

    jobs = career_assistant.job_recommender.run(
        f"Based on this parsed data, recommend jobs:\n{parsed}"
    ).content

    advice = career_assistant.career_coach.run(
        "Provide career guidance."
    ).content

    return {
        "parsed_resume": parsed,
        "job_recommendations": jobs,
        "career_advice": advice
    }
