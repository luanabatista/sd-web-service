from pydantic import BaseModel
from typing import Optional

from Model.Pessoa import Pessoa

class Passagem(BaseModel):
    id: Optional[int] = None
    pessoa: Pessoa
    id_voo: int
    cadeira: int
