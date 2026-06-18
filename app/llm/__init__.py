from dataclasses import dataclass
from typing import Any, TypeVar, overload

import httpx
from browser_use import ChatOpenAI
from browser_use.llm.messages import BaseMessage
from browser_use.llm.views import ChatInvokeCompletion
from pydantic import BaseModel

from app.config import settings
from app.llm.parsing import parse_structured_agent_json

T = TypeVar("T", bound=BaseModel)


def wrap_output_format(output_format: type[T]) -> type[T]:
    """Normalize LM Studio markdown JSON before pydantic validation."""

    class NormalizedOutputFormat(output_format):
        @classmethod
        def model_validate_json(
            cls,
            json_data: str | bytes | bytearray,
            *,
            strict: bool | None = None,
        ) -> T:
            if isinstance(json_data, (bytes, bytearray)):
                text = json_data.decode()
            else:
                text = str(json_data)
            return super().model_validate_json(parse_structured_agent_json(text), strict=strict)

    NormalizedOutputFormat.__name__ = output_format.__name__
    NormalizedOutputFormat.__qualname__ = output_format.__qualname__
    return NormalizedOutputFormat


@dataclass
class LMStudioChatOpenAI(ChatOpenAI):
    @overload
    async def ainvoke(
        self, messages: list[BaseMessage], output_format: None = None, **kwargs: Any
    ) -> ChatInvokeCompletion[str]: ...

    @overload
    async def ainvoke(
        self, messages: list[BaseMessage], output_format: type[T], **kwargs: Any
    ) -> ChatInvokeCompletion[T]: ...

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        output_format: type[T] | None = None,
        **kwargs: Any,
    ) -> ChatInvokeCompletion[T] | ChatInvokeCompletion[str]:
        if output_format is not None:
            output_format = wrap_output_format(output_format)
        return await super().ainvoke(messages, output_format=output_format, **kwargs)


def build_llm() -> LMStudioChatOpenAI:
    """LM Studio exposes an OpenAI-compatible API at localhost:1234/v1."""
    return LMStudioChatOpenAI(
        model=settings.lmstudio_model,
        base_url=settings.lmstudio_base_url,
        api_key=settings.lmstudio_api_key,
        temperature=0.1,
        timeout=httpx.Timeout(settings.lmstudio_request_timeout, connect=30.0),
        max_completion_tokens=settings.lmstudio_max_completion_tokens,
        add_schema_to_system_prompt=settings.lmstudio_add_schema_to_system_prompt,
        dont_force_structured_output=settings.lmstudio_dont_force_structured_output,
        remove_min_items_from_schema=True,
        remove_defaults_from_schema=True,
    )
