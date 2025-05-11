FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install system dependencies with cleanup
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    curl \
    python3.10 \
    python3.10-distutils \
    python3-pip \
    && ln -s /usr/bin/python3.10 /usr/bin/python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with version pinning
RUN pip install --no-cache-dir \
    transformers \
    torch==2.1.0 \
    accelerate==0.24.1 \
    sentencepiece==0.1.99 \
    fastapi==0.103.1 \
    uvicorn[standard]==0.23.2 \
    python-multipart==0.0.6 \
    pydantic==2.4.2 \
    watchdog==3.0.0 \
    && pip cache purge

# Verify CUDA is properly accessible
RUN python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); \
    print(f'Number of GPUs: {torch.cuda.device_count()}')"

# Create and set working directory
WORKDIR /app

RUN git clone https://huggingface.co/microsoft/phi-2 /app/phi-2 && \
    cd /app/phi-2 && \
    git lfs pull

# Copy application code
COPY app.py /app/

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

EXPOSE 8000

# Run with auto-reload and explicit workers
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", \
    "--reload", "--reload-dir", "/app", "--workers", "1"]