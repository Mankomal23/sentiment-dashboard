---
title: Sentiment Dashboard
emoji: 🧠
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Real-Time Sentiment Dashboard
NLP pipeline with live WebSocket streaming.

# 🧠 Real-Time Sentiment Intelligence Dashboard

A production-grade NLP pipeline that analyzes text sentiment in real time, streams results via WebSockets, and visualizes live trends on an interactive dashboard.

---

## 🎯 What is this?

Businesses receive thousands of customer reviews, support messages, and social media mentions daily — but lack tools to monitor sentiment shifts as they happen.

This project solves that by building a **live sentiment analysis system** that:
- Accepts text input (typed, uploaded CSV, or demo stream)
- Classifies each text as **Positive**, **Negative**, or **Neutral** using a transformer model
- Detects the **topic** of each text (product quality, delivery, customer service, etc.)
- Streams results to a live dashboard via **WebSockets** — no page refresh needed
- Shows real-time **trend charts** and **distribution graphs**

---

## 💡 How it Works

### 1. Model
Uses **Cardiff RoBERTa** (`cardiffnlp/twitter-roberta-base-sentiment-latest`) — a transformer model fine-tuned on 124 million tweets for 3-class sentiment classification:

```
Input Text
    │
    ▼
Cardiff RoBERTa (HuggingFace Transformers)
    │
    ├── Positive (score: 0.0 – 1.0)
    ├── Negative (score: 0.0 – 1.0)
    └── Neutral  (score: 0.0 – 1.0)
```

Low-confidence predictions (score < 0.65) are classified as **Neutral** to avoid false positives.

### 2. Topic Detection
Keyword-based topic tagging across 5 categories:
- Product Quality
- Customer Service
- Delivery
- Price & Value
- User Experience

### 3. Real-Time Streaming
Results are broadcast to all connected clients via **WebSockets** — the dashboard updates instantly without polling.

```
Text Input (typed / CSV / demo)
        │
        ▼
FastAPI Backend
        │
        ▼
HuggingFace Inference Pipeline
        │
        ▼
WebSocket Broadcast
        │
        ▼
Live Dashboard (charts + feed)
```

---

## 🏗️ Architecture

```
User Input
    │
    ▼
FastAPI (POST /analyze)
    ├── SentimentPipeline.analyze(text)
    │       ├── Cardiff RoBERTa inference
    │       ├── Topic detection
    │       └── Returns { sentiment, score, topics, latency_ms }
    └── WebSocket broadcast → all connected clients
                │
                ▼
        React-style Dashboard
            ├── Live Feed
            ├── Sentiment Trend Chart
            └── Distribution Donut Chart
```

---

## 🚀 Quick Start

### Local

```bash
# Install dependencies
pip install -r requirements.txt

# Copy frontend
mkdir backend/static
cp frontend/index.html backend/static/

# Start server
cd backend
uvicorn main:app --reload --port 8000

# Open dashboard
# http://localhost:8000
```

### Docker

```bash
docker build -t sentiment-dashboard .
docker run -p 7860:7860 sentiment-dashboard
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/analyze` | Analyze a single text |
| `POST` | `/analyze/batch` | Analyze a list of texts |
| `POST` | `/upload` | Upload CSV (one text per line) |
| `GET` | `/demo/start` | Start auto demo stream |
| `GET` | `/health` | Check model status |
| `WS` | `/ws` | WebSocket for live results |

### Sample Request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely amazing!"}'
```

### Sample Response

```json
{
  "id": "a3f1c2d4",
  "text": "This product is absolutely amazing!",
  "sentiment": "positive",
  "score": 0.9821,
  "topics": ["product quality"],
  "latency_ms": 243.5,
  "timestamp": 1746123456789
}
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| NLP Model | Cardiff RoBERTa (HuggingFace Transformers) |
| Backend | FastAPI + Uvicorn |
| Real-Time | WebSockets |
| Frontend | Vanilla JS + Chart.js |
| Charts | Chart.js 4.x |
| Deployment | Docker / HuggingFace Spaces |

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Model | cardiffnlp/twitter-roberta-base-sentiment-latest |
| Classes | Positive / Negative / Neutral |
| Training Data | 124M tweets |
| Throughput | ~500 texts/minute (CPU) |
| Latency | ~250ms per text (CPU) |

---

## 📁 Project Structure

```
sentiment-dashboard/
├── backend/
│   ├── main.py          # FastAPI app + WebSocket endpoint
│   ├── pipeline.py      # HuggingFace inference pipeline
│   ├── requirements.txt
│   └── static/
│       └── index.html   # Dashboard UI
├── frontend/
│   └── index.html       # Source frontend
├── Dockerfile
└── README.md
```

---

## 🔮 Future Improvements

- **Live Reddit/Twitter feed** — stream real posts from any subreddit
- **Multilingual support** — swap to mBERT for non-English text
- **Alert system** — notify when sentiment drops below threshold
- **Fine-tuning** — adapt model to domain-specific vocabulary
- **Redis queue** — decouple ingestion from inference for scale

---

## 📄 License

MIT © 2025