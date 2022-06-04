from pydantic import BaseModel

class FinalizaCompra(BaseModel):
    quant_pessoas: str
    dados_pessoas: str
    id_ida: str
    id_volta: str
    nome_cartao: str
    num_cartao: str
    crv: str
    parcelas: str
    venc_cartao: str
    valor_total: str