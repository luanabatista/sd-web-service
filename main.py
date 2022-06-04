from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from typing import Optional
from numpy import double, number
from Model.FinalizaCompra import FinalizaCompra
import json
from Model.Pessoa import Pessoa

origins = ["http://localhost:4200"]

middleware = [
    Middleware(CORSMiddleware, 
               allow_origins=origins,
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"],
               )
]

app = FastAPI(middleware=middleware)

with open('hospedagens.json', 'r' ) as f:
    hospedagens = json.load(f)
with open('voos.json', 'r' ) as f:
    voos = json.load(f)
with open('passagens.json', 'r' ) as f:
    passagens = json.load(f)
with open('compras.json', 'r' ) as f:
    compras = json.load(f)

def procuraVoo(origem, destino, data):
    opcoesVoos = []
    for v in voos:
        if origem == v['origem']:
            if destino == v['destino']:
                if data in v['data']:
                    opcoesVoos.append(v)
    return opcoesVoos

def geraNumId(dict):
    if dict:
        return max([d['id'] for d in dict]) + 1
    else: 
        return 1

def procuraVooPorId(id_voo):
    for v in voos:
        if id_voo == v['id']:
            return v

def procuraHospedagemPorId(id_hospedagem):
    for h in hospedagens:
        if id_hospedagem == h['id']:
            return h

@app.get('/passagens/busca')
def busca_voo(ida_e_volta: bool, origem: str, destino: str, data_ida: str, data_volta: Optional[str], quant_pessoas: int ):

    print(ida_e_volta, origem, destino, data_ida, data_volta, quant_pessoas)
    print(type(ida_e_volta), type(origem), type(destino), type(data_ida), type(data_volta), type(quant_pessoas))
    if ida_e_volta:
        voosIda = procuraVoo(origem, destino, data_ida, quant_pessoas)
        voosVolta = procuraVoo(destino, origem, data_volta, quant_pessoas)
        print(voosIda, voosVolta)
        return voosIda, voosVolta
    else:
        voos = procuraVoo(origem, destino, data_ida, quant_pessoas)
        return voos

@app.get('/passagens/compra')
def compra (id_ida: int, id_volta: int, quant_pessoas: int):

    preco_ida = double(procuraVooPorId(id_ida)['preco_passagem'])
    preco_volta = double(procuraVooPorId(id_volta)['preco_passagem'])
    
    preco_total = quant_pessoas*preco_ida+quant_pessoas*preco_volta

    return preco_total

@app.post('/passagens/finalizar-compra')
def finalizar_compra(finalizaCompra: FinalizaCompra):

    array_dados_pessoas = finalizaCompra.dados_pessoas.split(',')
    print(array_dados_pessoas)
    print(finalizaCompra)
    quant_pessoas = int(finalizaCompra.quant_pessoas)

    print(array_dados_pessoas[0])

    passagens_compra = []
    while quant_pessoas>0:
        if bool(finalizaCompra.id_volta):
                nova_passagem = {
                    "id": geraNumId(passagens),
                    "pessoa": {
                        "nome": array_dados_pessoas[0],
                        "numero": array_dados_pessoas[1],
                        "idade": array_dados_pessoas[2]
                    },
                    "id_voo": finalizaCompra.id_ida,
                }
                passagens_compra.append(nova_passagem)

                nova_passagem = {
                    "id": geraNumId(passagens),
                    "pessoa": {
                        "nome": array_dados_pessoas[0],
                        "numero": array_dados_pessoas[1],
                        "idade": array_dados_pessoas[2]
                    },
                    "id_voo": finalizaCompra.id_ida,
                }
                array_dados_pessoas.pop(0)
                array_dados_pessoas.pop(0)
                array_dados_pessoas.pop(0)
                passagens_compra.append(nova_passagem)
        else:
            
                nova_passagem = {
                    "id": geraNumId(passagens),
                    "pessoa": {
                        "nome": array_dados_pessoas[0],
                        "numero": array_dados_pessoas[1],
                        "idade": array_dados_pessoas[2]
                    },
                    "id_voo": finalizaCompra.id_ida,
                }
                array_dados_pessoas.pop(0)
                array_dados_pessoas.pop(0)
                array_dados_pessoas.pop(0)
                passagens_compra.append(nova_passagem)
        quant_pessoas=-1

    

    nova_compra = {
        "id": geraNumId(compras),
        "valor": finalizaCompra.valor_total,
        "itens": [passagens_compra],
        "dados_cartao": {
            "nome": finalizaCompra.nome_cartao,
            "numero": finalizaCompra.num_cartao,
            "crv": finalizaCompra.crv,
            "vencimento": finalizaCompra.venc_cartao },
        "parcelas": finalizaCompra.parcelas
    }

    compras.append(nova_compra)
    with open('compras.json', 'w') as f:
        json.dump(compras, f)

    passagens.append(nova_passagem)
    with open('passagens.json', 'w') as f:
        json.dump(passagens, f)

    return nova_compra

@app.get('/hospedagens/busca')
def busca_hospedagem(destino: str, data_entrada: str, data_saida: str, quant_pessoas: int, num_quartos: int ):
    opcoesHospedagens = []
    for h in hospedagens:
        if destino == h['destino']:
            opcoesHospedagens.append(h)
    return opcoesHospedagens

@app.get('/hospedagens/compra')
def compra_hospedagem(id_hospedagem: str, num_quartos: int, quant_pessoas: int):
    preco_diaria = double(procuraHospedagemPorId(id_hospedagem)['preco_diaria'])
    preco_total = quant_pessoas*preco_diaria

    return preco_total

@app.post('/hospedagens/finalizar-compra')
def finalizar_compra_hospedagem(finalizaCompra: FinalizaCompra):

    array_dados_pessoas = finalizaCompra.dados_pessoas.split(',')
    print(array_dados_pessoas)
    print(finalizaCompra)
    quant_pessoas = int(finalizaCompra.quant_pessoas)

    print(array_dados_pessoas[0])

    hospedagens_compra = []
    while quant_pessoas>0:
        if bool(finalizaCompra.id_volta):
                nova_hospedagem = {
                    "id": geraNumId(passagens),
                    "pessoa": {
                        "nome": array_dados_pessoas[0],
                        "numero": array_dados_pessoas[1],
                        "idade": array_dados_pessoas[2]
                    },
                    "id_quarto": array_dados_pessoas[3],
                }
                hospedagens_compra.append(nova_hospedagem)
                array_dados_pessoas.pop(0)
                array_dados_pessoas.pop(0)
                array_dados_pessoas.pop(0)
                array_dados_pessoas.pop(0)
        quant_pessoas=-1

    nova_compra = {
        "id": geraNumId(compras),
        "valor": finalizaCompra.valor_total,
        "itens": [hospedagens_compra],
        "dados_cartao": {
            "nome": finalizaCompra.nome_cartao,
            "numero": finalizaCompra.num_cartao,
            "crv": finalizaCompra.crv,
            "vencimento": finalizaCompra.venc_cartao },
        "parcelas": finalizaCompra.parcelas
    }

    compras.append(nova_compra)
    with open('compras.json', 'w') as f:
        json.dump(compras, f)

    passagens.append(nova_hospedagem)
    with open('hospedagens.json', 'w') as f:
        json.dump(hospedagens, f)

    return nova_compra