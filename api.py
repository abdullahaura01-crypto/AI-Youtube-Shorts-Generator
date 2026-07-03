from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import uuid

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/generate")
def generate(request: VideoRequest):
    job_id = str(uuid.uuid4())
    output_file = f"output_{job_id}.json"

    command = [
        "python",
        "main.py",
        request.url,
        "--output-json",
        output_file
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "output_file": output_file
    }
}