from pydantic import BaseModel
from typing import Optional

class Compra (BaseModel):
    id: Optional[int] = None
    valor: float
    parcelado: int
    id_dados_cartao: int
    itens: list #lista do que foi comprado