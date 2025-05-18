from typing import Literal

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    prompt: str


class LLMResponse(BaseModel):
    status: Literal["answered", "needs_more_context", "not_found"]
    answer: str
    requested_files: list[str]
