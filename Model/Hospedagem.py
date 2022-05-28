from pydantic import BaseModel
from typing import Optional

import datetime

class Hospedagem(BaseModel):
    id: Optional[int] = None
    nome: str
    cidade: str
    datas: list
    preco_hospedagem: float
    quartos: list