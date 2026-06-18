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
| `LMSTUDIO_REQUEST_TIMEOUT` | `300` | HTTP timeout per LLM request (seconds) |
| `LMSTUDIO_DONT_FORCE_STRUCTURED_OUTPUT` | `true` | Put JSON schema in prompt (better for LM Studio) |
| `AGENT_FLASH_MODE` | `true` | Minimal output schema — required for local models |
| `AGENT_USE_THINKING` | `false` | Prevents huge `thinking` JSON that gets truncated |
| `AGENT_MAX_CLICKABLE_ELEMENTS_LENGTH` | `8000` | Smaller DOM payload → faster, valid JSON |
| `AGENT_LLM_TIMEOUT` | `300` | browser-use per-step LLM timeout (default is 75s) |
| `AGENT_STEP_TIMEOUT` | `300` | Max seconds per agent step |
| `AGENT_ENABLE_PLANNING` | `false` | Skip extra planning LLM calls (faster locally) |
| `AGENT_MAX_STEPS` | `15` | Max browser actions per scrape |
| `AGENT_USE_VISION` | `false` | Send screenshots to Gemma 4 (much slower locally) |

If the model id differs on your machine, copy the exact string from the LM Studio server panel or `GET /v1/models`.

## Troubleshooting slow / timed-out runs

**Symptom:** `Invalid JSON: expected value at line 1` with `` ```json `` in the input

LM Studio wraps JSON in markdown fences and sometimes returns `action` as an object instead of an array. The app normalizes both automatically; you can also add to your prompt: raw JSON only, no code fences.

**Symptom:** `Invalid JSON: EOF while parsing` with `"thinking": "The us...`

Gemma 4's thinking mode dumps a huge `thinking` field into the JSON response, which gets cut off mid-object. Fixes:

1. Set `AGENT_FLASH_MODE=true` and `AGENT_USE_THINKING=false` (defaults above)
2. **Disable "Enable Thinking"** in LM Studio for this model
3. Set `LMSTUDIO_DONT_FORCE_STRUCTURED_OUTPUT=true`

**Symptom:** `LLM call timed out after 75 seconds`

browser-use defaults to a 75s LLM timeout (tuned for cloud APIs). A local 26B model often needs 2–5 minutes per step. The settings above raise that to 300s.

**Also check in LM Studio:**

1. **Disable "Enable Thinking"** on Gemma 4 — thinking tokens run before the answer and easily blow past timeouts.
2. **Keep `AGENT_USE_VISION=false`** unless you need screenshots — vision doubles payload size and inference time.
3. **Use focused `instructions`** — e.g. `"Find the follower count shown on the profile"` instead of asking to extract the whole page.
4. Watch LM Studio's server log while a scrape runs — if tokens/sec is very low, the model may still be loading or you're RAM-bound (16GB minimum for this model).
