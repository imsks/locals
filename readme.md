# Locals — Agentic System

Local LLM agents for the project. Minimal setup: **FastAPI** API + **browser-use** for browser automation + **LM Studio** for the LLM.

Default model: [google/gemma-4-26b-a4b-qat](https://lmstudio.ai/models/google/gemma-4-26b-a4b-qat) (Gemma 4 26B, tool-use + vision capable).

## Prerequisites

- Python **3.11+** (3.12 recommended; browser-use does not support 3.9/3.10)
- [uv](https://docs.astral.sh/uv/) or pip
- [LM Studio](https://lmstudio.ai/) with the model loaded and local server running
- Chromium (installed via browser-use)

## Quick start

```bash
cd locals

# 1. Virtual env (Python 3.12 via uv)
uv venv --python 3.12
source .venv/bin/activate

# 2. Dependencies
uv pip install -r requirements.txt
uvx browser-use install   # installs Playwright + Chromium

# 3. LM Studio
#    - Download & load google/gemma-4-26b-a4b-qat in LM Studio
#    - Local Server tab → Start Server (default http://localhost:1234)
#    - Confirm model id: curl http://localhost:1234/v1/models

# 4. Config
cp .env.example .env

# 5. Run API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## API

### Health

```bash
curl http://localhost:8080/api/v1/health
```

### Scrape a website

The agent opens a real browser, navigates to the URL, and extracts page content using your local LM Studio model.

```bash
curl -X POST http://localhost:8080/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "instructions": "Return the page title and first paragraph"
  }'
```

Response:

```json
{
  "url": "https://example.com",
  "task": "Go to https://example.com. Extract...",
  "result": "... extracted content ...",
  "steps_taken": 3
}
```

Interactive docs: http://localhost:8080/docs

## Project layout

```
locals/
├── app/
│   ├── main.py              # FastAPI entry
│   ├── config.py            # env settings
│   ├── llm.py               # LM Studio (OpenAI-compat) client
│   ├── agents/
│   │   └── scraper.py       # browser-use agent
│   └── routes/
│       ├── health.py
│       └── scrape.py
└── tests/
```

## Tests

```bash
pytest
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LMSTUDIO_BASE_URL` | `http://localhost:1234/v1` | LM Studio OpenAI-compatible API |
| `LMSTUDIO_API_KEY` | `lm-studio` | Dummy key (LM Studio ignores it) |
| `LMSTUDIO_MODEL` | `google/gemma-4-26b-a4b-qat` | Loaded model id from LM Studio |
| `AGENT_MAX_STEPS` | `15` | Max browser actions per scrape |
| `AGENT_USE_VISION` | `false` | Send screenshots to Gemma 4 (multimodal) |

If the model id differs on your machine, copy the exact string from the LM Studio server panel or `GET /v1/models`.
