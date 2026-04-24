# ClauseLens — production Dockerfile
# Lightweight Python image; runs Streamlit UI on port 8501.

FROM python:3.10-slim

# Metadata
LABEL org.opencontainers.image.title="ClauseLens" \
      org.opencontainers.image.description="Privacy-first AI contract risk analyzer. 100% local." \
      org.opencontainers.image.source="https://github.com/PavanUDD/clauselens" \
      org.opencontainers.image.licenses="MIT"

# System deps needed by PyMuPDF + FAISS + sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first (better Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Pre-download the embedding model so first run is instant
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

EXPOSE 8501

# Streamlit config — disable telemetry, bind to all interfaces
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app.py"]