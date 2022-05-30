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

with open('voos.json', 'r' ) as f:
    voos = json.load(f)
with open('passagens.json', 'r' ) as f:
    passagens = json.load(f)
with open('hospedagens.json', 'r' ) as f:
    hospedagens = json.load(f)
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

@app.post('/compra/passagem', status_code=201)
# id_voo, num_cadeira, nome_pessoa, idade_pessoa
def compra_passagem(nome_completo: str, idade: int, id_voo: int, cadeira: int, nome_cartao: str, 
                    num_cartao: str, crv: int, parcelas: int, venc_cartao):
    #na compra faz um post em passagem
    #post em compra 
    #e um put em voos

    #pega os dados da passagem, pega os dados da pessoa, dar o valor final e pega os dados do cartao
    #  depois disso fetua as alteraçoes em cada um


    nova_passagem = {
        "id": geraNumId(passagens),
        "pessoa": {
            "nome": nome_completo, 
            "idade": idade },
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


@app.get('/hospedagens/', status_code=200)
def get_hospedagens():
    return hospedagens

@app.get('/hospedagens/search', status_code=200)
def search_voo(nome: str = Query(None, title="Nome", description="The origem to filter for"),
               cidade: str = Query(None, title="Cidade", description="The destino to filter for")):
    opcoesHospedagens = []
    for h in hospedagens:
        if nome == h['origem']:
            if cidade == h['destino']:
                opcoesHospedagens.append(h)
    return opcoesHospedagens
    
'''
@app.put('/changePErson', status_code=204)
def change_person(person: Person):
    new_person = {
        "id": person.id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
    }

    person_list = [p for p in people if p['id'] == person.id]
    if len(person_list) > 0:
        people.remove(person_list[0])
        people.append(new_person)
        with open('people.json', 'w') as f:
            json.dump(people, f)
    else:
        return HTTPException(status_code=404, detail=f"Person with id {person.id} does not exist!")

@app.delete('/deletePerson/{p_id}', status_code=204)
def delete_person(p_id: int):
    person = [p for p in people if p['id'] == p_id]
    if len(person) > 0:
        people.remove(person[0])
        with open('people.json', 'w') as f:
            json.dump(people, f)
    else: 
        return HTTPException(status_code=404, detail=f"There is no person with id {p_id}")
        '''