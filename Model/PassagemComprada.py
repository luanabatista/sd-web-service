from pydantic import BaseModel
from typing import Optional

class PassagemComprada(BaseModel):
    id: Optional[int] = None
    id_pessoa: int
    id_voo: int
    
