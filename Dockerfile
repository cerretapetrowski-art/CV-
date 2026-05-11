FROM python:3.10-slim

WORKDIR /app

ENV DATA_DIR=/data
ENV TORCH_HOME=/app/.torch_cache

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install numpy==1.26.4

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data /app/uploads /app/.torch_cache

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
