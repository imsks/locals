import json
import re
from typing import Any

_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)


def strip_markdown_json(content: str) -> str:
    return _FENCE_PATTERN.sub("", content.strip()).strip()


def normalize_agent_output_dict(data: dict[str, Any]) -> dict[str, Any]:
    action = data.get("action")
    if isinstance(action, dict):
        data["action"] = [action]
    return data


def parse_structured_agent_json(content: str) -> str:
    payload = json.loads(strip_markdown_json(content))
    if not isinstance(payload, dict):
        raise ValueError("Agent output must be a JSON object")
    return json.dumps(normalize_agent_output_dict(payload))
