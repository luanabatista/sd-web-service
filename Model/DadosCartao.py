from pydantic import BaseModel
from typing import Optional

import datetime

class DadosCartao(BaseModel):
    nome: str
    numero: str
    crv: int
    vencimento: str