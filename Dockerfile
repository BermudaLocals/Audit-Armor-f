FROM python:3.11-slim
WORKDIR /app
# Pre-install core tools
RUN pip install --upgrade pip
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /app/backend
# Bind to the PORT env provided by Render
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
