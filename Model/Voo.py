from pydantic import BaseModel
from typing import Optional

import datetime

class Voo (BaseModel):
    id: Optional[int] = None
    origem: str
    destino: str
    data: datetime.datetime(int, int, int, int ,int)
    quant_cadeiras: int
    cadeiras_disp: list
    preco_passagem: float