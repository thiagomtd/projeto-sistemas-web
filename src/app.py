from flask import Flask, request
import pandas as pd
import json
import uuid


app = Flask(__name__)

# Adiciona usuário


@app.route("/user", methods=["POST"])
def create_user():

    response = json.loads(request.data)
    email = response["email"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["email"] == email:
            return {
                'statusCode': 302,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                "body": {
                    "message": "Email já cadastrado"
                }
            }
        else:
            users_data.append({
                "id": str(uuid.uuid1()),
                "nome": response["nome"],
                "email": response["email"],
                "senha": response["senha"],
                "tipo": response["tipo"],
                "materias": [],
                "duvidas": []
            })
            # todo: sobrescrever o conteudo do json
            return {
                'statusCode': 201,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                "body": {
                    "message": "Criado com sucesso"
                }
            }

    file.close()

#  Retorna todas as informações do usuario


@app.route("/user", methods=["GET"])
def get_user():
    response = json.loads(request.data)
    id = response["id"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                "body": {
                    "message": "Usuário encontrado sucesso",
                    "user": user
                }
            }
    return {
        'statusCode': 404,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": {
            "message": "Usuário não encontrado"
        }
    }

#  Realiza login


@app.route("/login", methods=["POST"])
def login():
    response = json.loads(request.data)
    email = response["email"]
    senha = response["senha"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["email"] == email:
            if user["senha"] == senha:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
                    },
                    "body": {
                        "message": "Login realizado com sucesso",
                        "data": {
                            "user_id": user["id"],
                            "user_name": user["nome"]
                        }
                    }
                }
            else:
                return {
                    'statusCode': 401,
                    'headers': {
                        'Access-Control-Allow-Headers': '*',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
                    },
                    "body": {
                        "message": "Senha incorreta"
                    }
                }
    file.close()
    return {
        'statusCode': 404,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": {
            "message": "Usuario não encontrado"
        }
    }

# Edita a lista de materias do aluno


@app.route("/materias", methods=["PUT"])
def editar_materias():
    response = json.loads(request.data)
    id = response["id"]
    materias = response["materias"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            # todo: Adicionar as novas materias no json
            user["materias"] = materias
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                "body": {
                    "message": "Materias adicionadas com sucesso",
                    "materias": user["materias"]
                }
            }

# Cria uma nova duvida


@app.route("/duvidas", methods=["POST"])
def create_duvida():
    response = json.loads(request.data)
    id = response["id"]
    duvida = response["duvida"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            user["duvidas"].append(
                {
                    "duvida_id": str(uuid.uuid1()),
                    "pergunta": duvida["pergunta"],
                    "materia": duvida["materia"],
                    "resposta": "",
                }
            )
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                "body": {
                    "message": "Duvida adicionada com sucesso",
                    "user": user
                }
            }

    return

#


@app.route("/duvidas", methods=["DELETE"])
def delete_duvidas():
    response = json.loads(request.data)
    id = response["id"]
    duvida_id = response["duvida_id"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            for duvida in user["duvidas"]:
                if duvida["duvida_id"] == duvida_id:

                    user["duvidas"].remove(duvida)

                    return {
                        'statusCode': 200,
                        'headers': {
                            'Access-Control-Allow-Headers': '*',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': '*'
                        },
                        "body": {
                            "message": "Duvida removida com sucesso",
                            "user": user
                        }
                    }
