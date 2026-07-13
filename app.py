from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from llama_cpp import Llama
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Model Load (Ensure path is correct)
# TinyLlama-1.1B Q4_K_M is approx 600MB, for <200MB 
# use Q2_K or smaller models if strictly limited.
llm = Llama(model_path="model/model.gguf", n_ctx=512)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/ask")
async def ask_ai(data: dict):
    prompt = data.get("prompt", "")
    output = llm(f"USER: {prompt} ASSISTANT:", max_tokens=128)
    response = output["choices"][0]["text"]
    return {"response": response}

# Copy function for API integration
def copy_to_clipboard(text):
    import pyperclip
    pyperclip.copy(text)
    return True

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
