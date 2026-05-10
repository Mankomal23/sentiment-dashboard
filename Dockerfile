FROM python:3.11-slim

WORKDIR /app

# Install deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ ./

# Copy frontend (served as static files)
COPY frontend/ ./static/

# Serve frontend from FastAPI
RUN echo "from fastapi.staticfiles import StaticFiles\nfrom fastapi.responses import FileResponse" >> /dev/null

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
