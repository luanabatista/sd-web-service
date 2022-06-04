from pydantic import BaseModel

class DadosCartao(BaseModel):
    nome: str
    numero: str
    crv: int
    vencimento: str