from pydantic import BaseModel
from typing import Optional

class Pessoa (BaseModel):
    nome: str
    idade: int
    numero: str