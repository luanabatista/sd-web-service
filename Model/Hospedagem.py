from pydantic import BaseModel
from typing import Optional

class Hospedagem(BaseModel):
    id: Optional[int] = None
    nome: str
    cidade: str
    preco_diaria: float