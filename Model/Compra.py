from pydantic import BaseModel
from typing import Optional

import datetime

from Model.DadosCartao import DadosCartao
from Model.Passagem import Passagem

class Compra (BaseModel):
    id: Optional[int] = None
    valor: float
    itens: list #lista do que foi comprado
    dados_cartao: DadosCartao
    parcelas: int
