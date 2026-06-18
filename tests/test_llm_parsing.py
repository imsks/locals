import json

import pytest

from app.llm.parsing import normalize_agent_output_dict, parse_structured_agent_json, strip_markdown_json


def test_strip_markdown_json_removes_fences() -> None:
    raw = '```json\n{"memory": "ok", "action": []}\n```'
    assert strip_markdown_json(raw) == '{"memory": "ok", "action": []}'


def test_normalize_agent_output_dict_wraps_action_object() -> None:
    data = {"memory": "done", "action": {"done": {"text": "552 followers", "success": True}}}
    normalized = normalize_agent_output_dict(data)
    assert normalized["action"] == [{"done": {"text": "552 followers", "success": True}}]


def test_parse_structured_agent_json_handles_lmstudio_response() -> None:
    content = """```json
{
  "memory": "The page has loaded.",
  "action": {
    "done": {
      "text": "imsks has 552 followers.",
      "success": true,
      "files_to_display": null
    }
  }
}
```"""
    parsed = json.loads(parse_structured_agent_json(content))
    assert parsed["action"][0]["done"]["text"] == "imsks has 552 followers."
