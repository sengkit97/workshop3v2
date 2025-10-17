from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from dotenv import load_dotenv
import uvicorn

# Load .env
load_dotenv()

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad") 

# Create pipeline **with the already loaded model and tokenizer**
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# FastAPI app
app = FastAPI()

class ChatRequest(BaseModel):
    question: str
    context: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = qa_pipeline(question=request.question, context=request.context)
        return ChatResponse(answer=result['answer'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
