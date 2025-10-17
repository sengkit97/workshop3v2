# -------------------------------
# Stage 1: Builder
# -------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies (temporarily)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# -------------------------------
# Stage 2: Runtime (small final image)
# -------------------------------
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only needed artifacts
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Expose port 8000
EXPOSE 8000
# Use a minimal entrypoint and CMD
ENTRYPOINT ["python"]
CMD ["day02.py"]
