import asyncio, os, random, time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pipeline import SentimentPipeline

app = FastAPI(title="Sentiment Dashboard API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
pipeline = SentimentPipeline()

class ConnectionManager:
    def __init__(self): self.active = []
    async def connect(self, ws):
        await ws.accept(); self.active.append(ws)
    def disconnect(self, ws):
        if ws in self.active: self.active.remove(ws)
    async def broadcast(self, data):
        dead = []
        for ws in self.active:
            try: await ws.send_json(data)
            except: dead.append(ws)
        for ws in dead:
            if ws in self.active: self.active.remove(ws)

manager = ConnectionManager()

class TextInput(BaseModel): text: str
class BatchInput(BaseModel): texts: list[str]

@app.post("/analyze")
async def analyze_text(body: TextInput):
    result = pipeline.analyze(body.text)
    await manager.broadcast(result); return result

@app.post("/analyze/batch")
async def analyze_batch(body: BatchInput):
    results = [pipeline.analyze(t) for t in body.texts]
    for r in results: await manager.broadcast(r); await asyncio.sleep(0.05)
    return {"results": results, "count": len(results)}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    texts = [l.strip() for l in content.decode("utf-8").splitlines() if l.strip()][:200]
    results = []
    for text in texts:
        r = pipeline.analyze(text); results.append(r)
        await manager.broadcast(r); await asyncio.sleep(0.02)
    return {"processed": len(results), "results": results}

@app.get("/health")
def health(): return {"status": "ok", "model": pipeline.model_name}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect: manager.disconnect(ws)

DEMO_TEXTS = [
    "This product is absolutely amazing, exceeded all my expectations!",
    "Terrible customer service, waited 3 hours and got no help.",
    "It's okay, nothing special but does the job.",
    "Best purchase I've made this year, highly recommend!",
    "Disappointed with the quality. Returned immediately.",
    "Outstanding support team, resolved my issue in minutes.",
    "Not worth the price. Would not buy again.",
    "Solid product, delivery was fast and packaging was great.",
]

@app.get("/demo/start")
async def start_demo():
    asyncio.create_task(_demo_stream()); return {"message": "Demo stream started"}

async def _demo_stream():
    for _ in range(20):
        result = pipeline.analyze(random.choice(DEMO_TEXTS))
        await manager.broadcast(result); await asyncio.sleep(1.5)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    @app.get("/")
    def serve_frontend(): return FileResponse(os.path.join(STATIC_DIR, "index.html"))
