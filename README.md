# Chatbot cli

## Prereqs
 - You need a `OPENAI_API_KEY` or to setup the `local_llm` (instruction for that in the local_llm folder)
 ```
    export OPENAI_API_KEY=<your_api_key>
 ```

## Quickstart

### 1. Build
```
    docker build . -t chatbot
```

### 2. Run
```
    docker run -it --rm chatbot
```

## Streamlit

With streamlit you cannot use local_llm only OPENAI (locally it would be possible to use the local llm, but since I will deploy it, it would be unavailable there)

### 1. Run it locally
Here you will need to install the deps with poetry (with the poetry shell pluggin)
```
    pip install poetry-plugin-shell
    poetry init
    poetry install
    poetry shell 
```
Then run:
```
    streamlit run streamlit_app.py
```

### 1.1 Run it locally with docker
No need to poetry install here, just run:
```
    docker build -f Dockerfile.streamlit -t streamlit-app .
    docker run -p 8501:8501 streamlit-app
```