# --- app/main.py ---
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import torch
from transformers import pipeline

from utils import apply_model

app = FastAPI()

class NERRequest(BaseModel):
    text: str

device = 0 if torch.cuda.is_available() else -1
ner_pipeline = pipeline("token-classification", model="CyberPeace-Institute/SecureBERT-NER", device=device)

@app.post("/ner")
async def ner(request: NERRequest):
    try:
        answer = apply_model([[request.text]], ner_pipeline)[0][0]
        return [{"entity": x["entity"], "word": x["word"]} for x in answer]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)