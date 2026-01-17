from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os, hashlib, datetime, json

app = FastAPI(title="Audit Armor Intelligence")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    # Looking for index.html in the same directory as main.py or one level up (root)
    paths = ["index.html", "../index.html", "frontend/index.html"]
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>Audit Armor: UI Source Not Found</h1>"

@app.get("/api/v1/governance")
async def get_gov():
    return {"standard": "Beyond Reasonable Doubt", "threshold": 0.98}
