from fastapi import FastAPI, Query, HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from typing import Optional

from numpy import append, double
from Model.Compra import Compra

from Model.Voo import Voo
from Model.Passagem import Passagem
import datetime
from datetime import date, datetime

import json

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

def procuraVoo(origem, destino, data, quant_pessoas):
    opcoesVoos = []
    for v in voos:
        if origem == v['origem']:
            if destino == v['destino']:
                if data in v['data']:
                    if quant_pessoas <= len(v['cadeiras_disp']):
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


@app.get('/passagens/voos')
def get_voos():
    return voos

@app.get('/passagens/busca')
def busca_voo(ida_e_volta: bool = Query(None, title="IdaEVolta", description="The origem to filter for"),
              origem: str = Query(None, title="Origem", description="The origem to filter for"),
              destino: str = Query(None, title="Destino", description="The destino to filter for"),
              data_ida: str = Query(None, title="DataIda", description="The data to filter for"),
              data_volta: Optional[str] = Query(None, title="DataVolta", description="The origem to filter for"),
              quant_pessoas: int = Query(None, title="QuantPessoas", description="The origem to filter for")):

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
def compra (id_ida: int = Query(None, title="Destino", description="The destino to filter for"),
            id_volta: int = Query(None, title="DataIda", description="The data to filter for"),
            quant_pessoas: int = Query(None, title="DataIda", description="The data to filter for")):
    # faz um get com os id dos voos, e quant de pessoas, dai ja recebe o valor, eh so recolher os dados
    #envia os dados e realiza a compra, encaminha pra proxima pag q pega os dados do cartao 
    #retorna todos os dados da compra

    preco_ida = double(procuraVooPorId(id_ida)['preco_passagem'])
    preco_volta = double(procuraVooPorId(id_volta)['preco_passagem'])
    
    preco_total = quant_pessoas*preco_ida+quant_pessoas*preco_volta

    return preco_total


@app.post('/passagens/finalizar-compra')
def compra_passagem(quant_pessoas: int, dados_pessoas: list, id_voo: int, nome_cartao: str, 
                    num_cartao: str, crv: int, parcelas: int, venc_cartao):
    passagens_compra = []
    for p in dados_pessoas:
        nova_passagem = {
            "id": geraNumId(passagens),
            "pessoa": {
                "nome": p.nome_completo, 
                "idade": p.idade,
                "numero": p.num_pessoa},
            "id_voo": id_voo,
            "cadeira": p.cadeira
        }
        passagens_compra.append(nova_passagem)

    nova_compra = {
        "id": geraNumId(compras),
        "valor": procuraVooPorId(id_voo)['preco_passagem']*quant_pessoas,
        "itens": [passagens_compra],
        "dados_cartao": {
            "nome": nome_cartao,
            "numero": num_cartao,
            "crv": crv,
            "vencimento": venc_cartao },
        "parcelas": parcelas
    }

    for v in voos:
        if id_voo == v['id']:
            for c in v['cadeiras_disp']:
                if c == p.cadeira:
                    v['cadeiras_disp'].remove(c)
    with open('voos.json', 'w') as f:
        json.dump(voos, f, indent=4)

    compras.append(nova_compra)
    with open('compras.json', 'w') as f:
        json.dump(compras, f)


    passagens.append(nova_passagem)
    with open('passagens.json', 'w') as f:
        json.dump(passagens, f)

    return nova_compra

@app.get('/hospedagens', status_code=200)
def get_hospedagens():
    return hospedagens
'''
@app.get('/hospedagens/busca', status_code=200)
def busca_voo( destino: str = Query(None, title="Destino", description="The destino to filter for"),
               data_entrada: str = Query(None, title="DataIda", description="The data to filter for"),
               data_saida: Optional[str] = Query(None, title="DataVolta", description="The origem to filter for"),
               num_quartos: int = Query(None, title="QuantPessoas", description="The origem to filter for")):

    def procuraHospedagem(destino, data_entrada, data_saida, num_quartos):
        opcoesHospedagens = []
        for h in hospedagens:
            if destino == h['destino']:
                if num_quartos <= len(h['quartos_disp']):
                    opcoesHospedagens.append(h)
        return opcoesHospedagens

    return procuraHospedagem(destino, data_entrada, data_saida, num_quartos)
    '''
