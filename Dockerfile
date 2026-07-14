FROM python:3.10-slim

# Install dependencies
RUN pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install fastapi uvicorn transformers jinja2

WORKDIR /app
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
