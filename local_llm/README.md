## Prerequisites

- Docker installed
- NVIDIA Docker runtime (for GPU acceleration)
- Git LFS installed (for model downloading)
- NVIDIA GPU with at least 8GB VRAM (recommended)

## Quick Start

### 1. Build

```
    	docker build -t local-llm .
```


### 2. Run

```
    	docker run --gpus all -p 8000:8000 local-llm
```

### 3. Test

```
    curl -X POST "http://localhost:8000/generate" \
        -H "Content-Type: application/json" \
        -d '{"question":"What is the capital of France?"}'
```

## Configuration Options

### Environment Variables

| Variable         | Default                        | Description                              |
|------------------|--------------------------------|------------------------------------------|
| `MODEL_REPO`     | `microsoft/phi-2`              | HuggingFace model repository             |
| `MAX_TOKENS`     | `200`                          | Maximum response length                  |
| `TEMPERATURE`    | `0.7`                          | Creativity/randomness of outputs         |
| `TOP_P`          | `0.9`                          | Nucleus sampling probability threshold   |
| `DEVICE`         | `auto`                         | Device to use (`cuda`, `cpu`, or `auto`) |

### Build Arguments

| Argument         | Example Value                  | Description                              |
|------------------|--------------------------------|------------------------------------------|
| `MODEL_REPO`     | `TinyLlama/TinyLlama-1.1B-Chat`| Model to download during build           |
| `EXTRA_PACKAGES` | `git-lfs,curl`                 | Additional system packages to install    |

### Runtime Flags

| Flag             | Example                       | Description                              |
|------------------|-------------------------------|------------------------------------------|
| `--gpus`         | `all`                         | GPU access for container                 |
| `--shm-size`     | `1g`                          | Shared memory size                       |
| `-e`             | `MAX_TOKENS=500`              | Override environment variables           |

Example usage with custom configuration:
```bash
docker build \
  --build-arg MODEL_REPO=TinyLlama/TinyLlama-1.1B-Chat \
  -t custom-llm .

docker run -d \
  --gpus all \
  --shm-size 1g \
  -e MAX_TOKENS=500 \
  -e TEMPERATURE=0.5 \
  -p 8000:8000 \
  custom-llm