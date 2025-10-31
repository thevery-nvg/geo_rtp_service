from typing import Dict
from pydantic import BaseModel

class NngDataWrite(BaseModel):
    passport: Dict[str, Dict[str, str]]
    coordinates: Dict[str, Dict[str, str]]
    control_places: Dict[str, Dict[str, str]]
    valves: Dict[str, Dict[str, str]]



class NngDataGet(BaseModel):
    reg_number: str
    year: str
