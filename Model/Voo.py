from pydantic import BaseModel
from typing import Optional

class Voo (BaseModel):
    id: Optional[int] = None
    origem: str
    destino: str
    data: str
    preco_passagem: float