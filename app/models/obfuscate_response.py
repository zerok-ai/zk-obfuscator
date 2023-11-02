from pydantic import BaseModel
from typing import Any, Dict


class Payload(BaseModel):
    data: Dict[str, Any]


class ObfuscateResponse(BaseModel):
    payload: Payload

    def to_dict(self):
        return self.dict()
