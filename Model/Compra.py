from pydantic import BaseModel
from typing import Optional
from Model.DadosCartao import DadosCartao

class Compra (BaseModel):
    id: Optional[int] = None
    valor: float
    itens: list #lista do que foi comprado
    dados_cartao: DadosCartao
    parcelas: int
