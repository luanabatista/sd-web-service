from datetime import date, datetime
from fastapi import FastAPI, Query, HTTPException
from typing import Optional

from numpy import append
from Model.Compra import Compra

from Model.Voo import Voo
from Model.Passagem import Passagem
import datetime

import json

app = FastAPI()

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

# 1 fazer classes
# 2 popular classes

# consulta de passagens aéreas - get
# compra de passagens aéreas - put
# consulta de hospedagem - get
# compra de hospedagem - put

#consulta todos os voos
@app.get('/voos', status_code=200)
def get_voos():
    return voos

#consulta voo por ida e volta, origem, destino, data de ida, data de volta, quant de pessoas
@app.get('/voos/busca', status_code=200)
def busca_voo(ida_e_volta: bool = Query(None, title="IdaEVolta", description="The origem to filter for"),
               origem: str = Query(None, title="Origem", description="The origem to filter for"),
               destino: str = Query(None, title="Destino", description="The destino to filter for"),
               data_ida: str = Query(None, title="DataIda", description="The data to filter for"),
               data_volta: Optional[str] = Query(None, title="DataVolta", description="The origem to filter for"),
               quant_pessoas: int = Query(None, title="QuantPessoas", description="The origem to filter for")):

    if ida_e_volta:
        voosIda = procuraVoo(origem, destino, data_ida, quant_pessoas)
        voosVolta = procuraVoo(destino, origem, data_volta, quant_pessoas)
        return voosIda, voosVolta
    else:
        voos = procuraVoo(origem, destino, data_ida, quant_pessoas)
        return voos

@app.post('/voos/compra-passagem', status_code=201)
def compra_passagem(nome_completo: str, idade: int, num_pessoa: str, id_voo: int, cadeira: int, nome_cartao: str, 
                    num_cartao: str, crv: int, parcelas: int, venc_cartao):

    #na compra faz um post em passagem
    #post em compra 
    #e um put em voos
    nova_passagem = {
        "id": geraNumId(passagens),
        "pessoa": {
            "nome": nome_completo, 
            "idade": idade,
            "numero": num_pessoa},
        "id_voo": id_voo,
        "cadeira": cadeira
    }

    nova_compra = {
        "id": geraNumId(compras),
        "valor": 100.00,
        "itens": [["P", nova_passagem.id]],
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
                if c == cadeira:
                    v['cadeiras_disp'].remove(c)
    with open('voos.json', 'w') as f:
        json.dump(voos, f, indent=4)

    compras.append(nova_compra)
    with open('compras.json', 'w') as f:
        json.dump(compras, f)


    passagens.append(nova_passagem)
    with open('passagens.json', 'w') as f:
        json.dump(passagens, f)


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
