FROM python:3.13-slim

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Paddle & YOLO configuration
ENV PADDLE_HOME=/root/.paddlex
RUN mkdir -p /app/.ultralytics

ENV YOLO_CONFIG_DIR=/app/.ultralytics
ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True

WORKDIR /app

# Install Linux packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Copy project
COPY . .

# Download PaddleOCR model
RUN python -c "from paddleocr import TextRecognition; TextRecognition(engine='paddle')"

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]