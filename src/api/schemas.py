from typing import Dict

from pydantic import BaseModel


class TransformRequest(BaseModel):
    value: str


class BatchRequest(BaseModel):
    data: Dict[str, str]
