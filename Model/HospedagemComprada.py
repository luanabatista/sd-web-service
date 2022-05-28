from pydantic import BaseModel
from typing import Optional

import datetime

class PassagemComprada(BaseModel):
    id: Optional[int] = None
    id_pessoa: int
    id_Hospedagem: int
    data_entrada: datetime.datetime(int, int, int, int ,int)
    data_saida: datetime.datetime(int, int, int, int ,int)