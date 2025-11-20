from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import shutil
import time
from utils import (
    read_document,
    find_links,
    get_github_context,
    get_portfolio_context,
    call_gemini_api,
    save_to_db,
    get_db_connection
)
from prompts import (
    PROMPT_TRIAGE,
    PROMPT_MATCHING_360,
    PROMPT_EXECUTIVE_SUMMARY,
    PROMPT_FEEDBACK
)
import config

app = FastAPI(title="Inter-sight API", description="AI-Powered Recruiting Backend")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Pydantic Models
class AnalysisRequest(BaseModel):
    job_description: str
    culture_values: str

class FeedbackRequest(BaseModel):
    candidate_id: str
    candidate_name: str
    job_title: str
    company_name: str
    analysis_json: dict

class ExecutiveSummaryRequest(BaseModel):
    analysis_json: dict
    culture_text: str

@app.get("/")
def read_root():
    return {"message": "Inter-sight API is running"}

@app.post("/analyze")
async def analyze_cvs(
    job_description: str = Form(...),
    culture_values: str = Form(...),
    files: List[UploadFile] = File(...)
):
    results = []
    
    if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "your-api-key-here":
        raise HTTPException(status_code=500, detail="API Key not configured")

    for file in files:
        try:
            # Save file
            timestamp = int(time.time())
            filename = f"{timestamp}_{file.filename}"
            save_path = os.path.join(UPLOAD_DIR, filename)
            
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Read content
            # We need to re-open the file or pass the path to read_document if it supports it
            # utils.read_document expects a streamlit UploadedFile or similar that has .read() or .seek()
            # FastAPI UploadFile has .file which is a SpooledTemporaryFile
            
            # Let's adapt read_document usage. 
            # Since we saved it, we can open it from disk or use the UploadFile object.
            # utils.read_document uses .name and .read(). 
            # Let's re-open the saved file to be safe and consistent with utils.
            
            with open(save_path, "rb") as f:
                # Mocking an object that has .name and .read() and .seek()
                class FileWrapper:
                    def __init__(self, f, name):
                        self.f = f
                        self.name = name
                    def read(self):
                        return self.f.read()
                    def seek(self, offset):
                        self.f.seek(offset)
                    def getbuffer(self):
                        return self.f.read() # fallback
                
                file_wrapper = FileWrapper(f, filename)
                cv_text = read_document(file_wrapper)

            if cv_text.startswith("Error:"):
                results.append({"filename": file.filename, "error": "Could not read file"})
                continue

            # Analysis Logic (Ported from app.py)
            found_links = find_links(cv_text)
            
            triage_prompt = PROMPT_TRIAGE.format(
                job_description=job_description,
                cv_text=cv_text
            )
            triage_json_str = call_gemini_api(triage_prompt)
            
            try:
                triage_json = json.loads(triage_json_str)
            except:
                triage_json = {}

            job_category = triage_json.get("job_category", "Other")
            urls_to_analyze = triage_json.get("urls_to_analyze", [])
            
            external_context = "N/A"
            if urls_to_analyze:
                first_url = urls_to_analyze[0]
                if job_category == "Tech" and "github" in first_url.lower():
                    external_context = get_github_context(first_url)
                elif job_category == "Design" and ("behance" in first_url.lower() or "dribbble" in first_url.lower()):
                    external_context = get_portfolio_context(first_url)

            analysis_360_prompt = PROMPT_MATCHING_360.format(
                job_and_culture_text=f"{job_description}\n{culture_values}",
                cv_text=cv_text,
                external_context=external_context
            )
            analysis_360_str = call_gemini_api(analysis_360_prompt)
            
            try:
                analysis_360 = json.loads(analysis_360_str)
            except json.JSONDecodeError:
                results.append({"filename": file.filename, "error": "Failed to parse analysis JSON"})
                continue

            # Save to DB
            save_to_db(
                filename=filename,
                filepath=save_path,
                analysis_json=analysis_360,
                feedback_email=None,
                status='analyzed'
            )

            results.append({
                "id": filename,
                "filename": file.filename,
                "analysis": analysis_360,
                "full_context": {
                    "cv_text": cv_text, # Maybe too large to send back?
                    "job_title": job_description.split('\n')[0],
                    "company_name": culture_values.split('\n')[0]
                }
            })

        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})

    return {"results": results}

@app.post("/feedback")
async def generate_feedback(request: FeedbackRequest):
    feedback_prompt = PROMPT_FEEDBACK.format(
        candidate_name=request.candidate_name,
        job_title=request.job_title,
        company_name=request.company_name,
        analysis_json=json.dumps(request.analysis_json)
    )
    feedback_email = call_gemini_api(feedback_prompt)
    return {"email_body": feedback_email}

@app.post("/executive-summary")
async def generate_summary(request: ExecutiveSummaryRequest):
    summary_prompt = PROMPT_EXECUTIVE_SUMMARY.format(
        analysis_json=json.dumps(request.analysis_json),
        culture_text=request.culture_text
    )
    summary = call_gemini_api(summary_prompt)
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
