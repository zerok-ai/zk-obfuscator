from pydantic import BaseModel
from typing import Any, Dict


class ObfuscateRequest(BaseModel):
    data: Dict[str, Any]
    language: str
