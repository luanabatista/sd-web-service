from pydantic import BaseModel
from typing import Optional

class Pessoa (BaseModel):
    id: Optional[int] = None
    nome: str
    idade: int