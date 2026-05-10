# Real-Time Sentiment Dashboard

## Quick Start (Docker)
```bash
docker build -t sentiment-dashboard .
docker run -p 8000:8000 sentiment-dashboard
# Open http://localhost:8000
```

## Quick Start (Local)
```bash
cd backend
pip install -r requirements.txt
mkdir static && cp ../frontend/index.html static/
uvicorn main:app --reload
# Open http://localhost:8000
```

## Deploy to Railway/Render
1. Push to GitHub
2. Connect repo on railway.app or render.com
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy — done.

## Endpoints
- `GET  /`             — Dashboard UI
- `POST /analyze`      — Analyze single text
- `POST /analyze/batch`— Analyze list of texts
- `POST /upload`       — Upload CSV (one text per line)
- `GET  /demo/start`   — Start auto demo stream
- `WS   /ws`           — WebSocket for live results
