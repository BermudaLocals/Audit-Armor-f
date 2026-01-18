from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
import hashlib
import datetime
import json
from pathlib import Path

app = FastAPI(
    title="Audit Armor Intelligence",
    description="Governance Intelligence Platform API",
    version="2.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory for audit chain
DATA_DIR = os.getenv("DATA_DIR", "/tmp/audit_armor_data")
os.makedirs(DATA_DIR, exist_ok=True)

# Demo data
DEMO_SHIPS = [
    {"id": "ship-001", "name": "Alpha Prime", "fleet": "Alpha", "tenants": 78, "status": "governed", "compliance": 99.8},
    {"id": "ship-002", "name": "Alpha Secondary", "fleet": "Alpha", "tenants": 82, "status": "governed", "compliance": 99.5},
    {"id": "ship-003", "name": "Alpha Tertiary", "fleet": "Alpha", "tenants": 76, "status": "governed", "compliance": 99.9},
    {"id": "ship-004", "name": "Alpha Quaternary", "fleet": "Alpha", "tenants": 76, "status": "governed", "compliance": 99.2},
    {"id": "ship-005", "name": "Beta Prime", "fleet": "Beta", "tenants": 65, "status": "governed", "compliance": 98.9},
    {"id": "ship-006", "name": "Beta Secondary", "fleet": "Beta", "tenants": 58, "status": "governed", "compliance": 99.1},
    {"id": "ship-007", "name": "Beta Tertiary", "fleet": "Beta", "tenants": 62, "status": "warning", "compliance": 97.8},
    {"id": "ship-008", "name": "Beta Quaternary", "fleet": "Beta", "tenants": 55, "status": "governed", "compliance": 98.5},
    {"id": "ship-009", "name": "Beta Quintary", "fleet": "Beta", "tenants": 58, "status": "governed", "compliance": 99.0},
    {"id": "ship-010", "name": "Gamma Prime", "fleet": "Gamma", "tenants": 85, "status": "governed", "compliance": 97.2},
    {"id": "ship-011", "name": "Gamma Secondary", "fleet": "Gamma", "tenants": 78, "status": "warning", "compliance": 96.8},
    {"id": "ship-012", "name": "Gamma Tertiary", "fleet": "Gamma", "tenants": 74, "status": "governed", "compliance": 97.5},
]

DEMO_TASKS = [
    {"id": "task-001", "title": "Quarterly Compliance Review", "due": "2026-01-25", "priority": "high", "status": "pending"},
    {"id": "task-002", "title": "Tenant Onboarding Verification", "due": "2026-01-20", "priority": "medium", "status": "in_progress"},
    {"id": "task-003", "title": "Security Audit Documentation", "due": "2026-01-30", "priority": "low", "status": "pending"},
    {"id": "task-004", "title": "Fleet Alpha Inspection", "due": "2026-02-01", "priority": "medium", "status": "pending"},
    {"id": "task-005", "title": "Annual Governance Report", "due": "2026-02-15", "priority": "high", "status": "pending"},
]

def log_to_chain(event: str, data: dict):
    """Append event to immutable audit chain"""
    log_path = os.path.join(DATA_DIR, "audit_chain.jsonl")
    prev_hash = "0" * 64
    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            lines = f.readlines()
            if lines:
                prev_hash = json.loads(lines[-1])["hash"]
    entry = {
        "ts": datetime.datetime.utcnow().isoformat(),
        "event": event,
        "data": data,
        "prev": prev_hash
    }
    entry["hash"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

# Health check
@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "service": "Audit Armor", "version": "2.0.0"}

# Governance endpoint
@app.get("/api/v1/governance")
async def get_governance():
    return {
        "standard": "Beyond Reasonable Doubt",
        "threshold": 0.98,
        "status": "Governed",
        "last_audit": "2026-01-15T10:30:00Z",
        "next_audit": "2026-02-15T10:30:00Z"
    }

# Score endpoint
@app.get("/api/v1/score")
async def get_score():
    total_tenants = sum(ship["tenants"] for ship in DEMO_SHIPS)
    avg_compliance = sum(ship["compliance"] for ship in DEMO_SHIPS) / len(DEMO_SHIPS)
    return {
        "overall_score": round(avg_compliance, 1),
        "total_ships": len(DEMO_SHIPS),
        "total_tenants": total_tenants,
        "governed_ships": len([s for s in DEMO_SHIPS if s["status"] == "governed"]),
        "warning_ships": len([s for s in DEMO_SHIPS if s["status"] == "warning"]),
        "critical_ships": len([s for s in DEMO_SHIPS if s["status"] == "critical"])
    }

# Ships endpoint
@app.get("/api/v1/ships")
async def get_ships():
    return {"ships": DEMO_SHIPS, "total": len(DEMO_SHIPS)}

# Single ship endpoint
@app.get("/api/v1/ships/{ship_id}")
async def get_ship(ship_id: str):
    ship = next((s for s in DEMO_SHIPS if s["id"] == ship_id), None)
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship

# Fleets endpoint
@app.get("/api/v1/fleets")
async def get_fleets():
    fleets = {}
    for ship in DEMO_SHIPS:
        fleet_name = ship["fleet"]
        if fleet_name not in fleets:
            fleets[fleet_name] = {"name": fleet_name, "ships": [], "total_tenants": 0, "avg_compliance": 0}
        fleets[fleet_name]["ships"].append(ship)
        fleets[fleet_name]["total_tenants"] += ship["tenants"]
    
    for fleet in fleets.values():
        fleet["avg_compliance"] = round(sum(s["compliance"] for s in fleet["ships"]) / len(fleet["ships"]), 1)
        fleet["ship_count"] = len(fleet["ships"])
    
    return {"fleets": list(fleets.values())}

# Tasks endpoint
@app.get("/api/v1/tasks")
async def get_tasks():
    return {"tasks": DEMO_TASKS, "total": len(DEMO_TASKS)}

# CEO Dashboard
@app.get("/api/v1/dashboard/ceo")
async def get_ceo_dashboard():
    total_tenants = sum(ship["tenants"] for ship in DEMO_SHIPS)
    avg_compliance = sum(ship["compliance"] for ship in DEMO_SHIPS) / len(DEMO_SHIPS)
    return {
        "role": "CEO",
        "summary": {
            "governance_score": round(avg_compliance, 1),
            "total_ships": len(DEMO_SHIPS),
            "total_tenants": total_tenants,
            "active_tasks": len([t for t in DEMO_TASKS if t["status"] != "completed"]),
            "compliance_status": "Beyond Reasonable Doubt"
        },
        "alerts": [
            {"type": "warning", "message": "2 ships require attention", "timestamp": "2026-01-17T10:00:00Z"}
        ]
    }

# Deep Dashboard (detailed view)
@app.get("/api/v1/dashboard/deep")
async def get_deep_dashboard():
    return {
        "role": "Auditor",
        "ships": DEMO_SHIPS,
        "tasks": DEMO_TASKS,
        "audit_chain_length": len(open(os.path.join(DATA_DIR, "audit_chain.jsonl")).readlines()) if os.path.exists(os.path.join(DATA_DIR, "audit_chain.jsonl")) else 0
    }

# Updates/notifications endpoint
@app.get("/api/v1/updates")
async def get_updates():
    return {
        "updates": [
            {"id": 1, "type": "info", "message": "System operating normally", "timestamp": "2026-01-17T12:00:00Z"},
            {"id": 2, "type": "success", "message": "Daily compliance check completed", "timestamp": "2026-01-17T06:00:00Z"},
            {"id": 3, "type": "warning", "message": "Ship Gamma Secondary requires review", "timestamp": "2026-01-16T14:30:00Z"}
        ]
    }

# Evidence upload
@app.post("/api/v1/evidence/upload")
async def upload_evidence(file: UploadFile = File(...)):
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    
    # Log to audit chain
    log_to_chain("EVIDENCE_UPLOAD", {
        "filename": file.filename,
        "sha256": file_hash,
        "size": len(content)
    })
    
    return {
        "id": file_hash[:12],
        "filename": file.filename,
        "status": "Admissible",
        "sha256": file_hash,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# Orbit data for visualization
@app.get("/api/v1/orbit")
async def get_orbit_data():
    return {
        "core": {"name": "Audit Armor Core", "status": "governed"},
        "ships": [{"id": s["id"], "name": s["name"], "status": s["status"], "tenants": s["tenants"]} for s in DEMO_SHIPS],
        "total_tenants": sum(s["tenants"] for s in DEMO_SHIPS)
    }

# Serve frontend - find the correct path
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    # Try multiple possible paths for the frontend
    possible_paths = [
        Path(__file__).parent.parent.parent / "frontend" / "index.html",  # /app/frontend/index.html
        Path("/app/frontend/index.html"),
        Path("../frontend/index.html"),
        Path("frontend/index.html"),
    ]
    
    for path in possible_paths:
        if path.exists():
            return HTMLResponse(content=path.read_text(encoding="utf-8"))
    
    # Fallback: return a simple HTML page
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head><title>Audit Armor</title></head>
    <body style="background:#1a0a0a;color:white;font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;">
        <div style="text-align:center;">
            <h1 style="color:#FF4500;">🛡️ Audit Armor API</h1>
            <p>API is running. Frontend not found.</p>
            <p>Try: <a href="/api/v1/health" style="color:#FF6B35;">/api/v1/health</a></p>
        </div>
    </body>
    </html>
    """)

# Catch-all for SPA routing
@app.get("/{path:path}", response_class=HTMLResponse)
async def serve_spa(path: str):
    # API routes should not reach here, but just in case
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Serve the main index for SPA routing
    return await serve_index()
