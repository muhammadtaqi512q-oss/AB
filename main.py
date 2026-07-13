from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline, AutoTokenizer
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize Model
print("⏳ Loading Ira AI Core Engine...")
model_id = 'Qwen/Qwen1.5-0.5B-Chat'
tokenizer = AutoTokenizer.from_pretrained(model_id)
ai_pipeline = pipeline('text-generation', model=model_id, tokenizer=tokenizer)
print("✅ Ira AI Engine Active!")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_endpoint(data: dict):
    user_message = data.get("message", "")
    custom_rules = data.get("custom_rules", "You are a helpful AI assistant.")
    
    if not user_message:
        return JSONResponse({"error": "Message is missing"}, status_code=400)

    full_prompt = f"<|im_start|>system\n{custom_rules}\n<|im_end|>\n<|im_start|>user\n{user_message}\n<|im_end|>\n<|im_start|>assistant\n"
    
    output = ai_pipeline(full_prompt, max_new_tokens=150, do_sample=True, pad_token_id=tokenizer.eos_token_id)
    response_text = output[0]['generated_text'].split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
    
    return {"status": "success", "response": response_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
