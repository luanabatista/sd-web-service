from pydantic import BaseModel
from typing import Optional

import datetime

class DadosCartao(BaseModel):
    id: Optional[int] = None
    numero: int
    crv: int
    vencimento: datetime.datetime(int, int)