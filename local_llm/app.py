from fastapi import FastAPI, HTTPException
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel
import torch

app = FastAPI()

model_path = "microsoft/phi-2"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {device}")

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    trust_remote_code=True
).to(device)
class QuestionRequest(BaseModel):
    question: str
    
@app.post("/generate")
async def generate(request: QuestionRequest):
    try:
        inputs = tokenizer(
            request.question,
            return_tensors="pt",
            return_attention_mask=False,
            truncation=True,
            max_length=512
        ).to("cuda")
        outputs = model.generate(**inputs, max_length=200)
        response = tokenizer.batch_decode(outputs)[0]
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))