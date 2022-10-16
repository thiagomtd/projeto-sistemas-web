from flask import Flask, jsonify, request
import json
import uuid
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

# Adiciona usuário


@app.route("/user", methods=["POST"])
def create_user():

    response = json.loads(request.data)
    email = response["email"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["email"] == email:
            data = jsonify({
                'statusCode': 302,
                "body": {
                    "message": "Email já cadastrado"
                }
            })
            data.headers.add('Access-Control-Allow-Headers', '*')
            data.headers.add('Access-Control-Allow-Origin', '*')
            data.headers.add("Access-Control-Allow-Methods", '*')

            return data
    file.close()
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
    with open("user_data.json", "w") as newFile:
        json.dump(users_data, newFile)

        data = jsonify(
            {
                'statusCode': 201,
                "body": {
                    "message": "Criado com sucesso"
                }
            }
        )
        data.headers.add('Access-Control-Allow-Headers', '*')
        data.headers.add('Access-Control-Allow-Origin', '*')
        data.headers.add("Access-Control-Allow-Methods", ' *')

        return data


#  Retorna todas as informações do usuario


@app.route("/user", methods=["GET"])
def get_user():

    id = request.args["id"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            data = jsonify({
                'statusCode': 200,
                "body": {
                    "message": "Usuário encontrado sucesso",
                    "user": user
                }
            })

            data.headers.add('Access-Control-Allow-Headers', '*')
            data.headers.add('Access-Control-Allow-Origin', '*')
            data.headers.add("Access-Control-Allow-Methods", ' *')
            return data

    data = jsonify({
        'statusCode': 404,
        "body": {
            "message": "Usuário não encontrado"
        }
    })

    data.headers.add('Access-Control-Allow-Headers', '*')
    data.headers.add('Access-Control-Allow-Origin', '*')
    data.headers.add("Access-Control-Allow-Methods", ' *')
    return data

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
            user["materias"] = materias
            with open("user_data.json", "w") as newFile:
                json.dump(users_data, newFile)
                data = jsonify({
                    'statusCode': 200,
                    "body": {
                        "message": "Materias adicionadas com sucesso",
                        "materias": user["materias"]
                    }
                })
                data.headers.add('Access-Control-Allow-Headers', '*')
                data.headers.add('Access-Control-Allow-Origin', '*')
                data.headers.add("Access-Control-Allow-Methods", ' *')
                return data

# Cria uma nova duvida


@app.route("/duvida", methods=["POST"])
def create_duvida():
    response = json.loads(request.data)
    id = response["id"]
    duvida = response["duvida"]

    print(duvida)

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            user["duvidas"].append(
                {
                    "id_duvida": str(uuid.uuid1()),
                    "pergunta": duvida["pergunta"],
                    "materia": duvida["materia"],
                    "resposta": "",
                }
            )
    with open("user_data.json", "w") as newFile:
        json.dump(users_data, newFile)
        data = jsonify({
            'statusCode': 200,
            "body": {
                "message": "Duvida adicionada com sucesso",
                "user": user
            }
        })

        data.headers.add('Access-Control-Allow-Headers', '*')
        data.headers.add('Access-Control-Allow-Origin', '*')
        data.headers.add("Access-Control-Allow-Methods", ' *')
        return data

#


@app.route("/duvida", methods=["DELETE"])
def delete_duvida():
    id = request.args["id"]
    id_duvida = request.args["id_duvida"]

    file = open('user_data.json')
    users_data = json.load(file)

    for user in users_data:
        if user["id"] == id:
            print(user["id"])
            for duvida in user["duvidas"]:
                print(duvida)
                if duvida["id_duvida"] == id_duvida:
                    user["duvidas"].remove(duvida)
                    with open("user_data.json", "w") as newFile:
                        json.dump(users_data, newFile)
                        data = jsonify({
                            'statusCode': 200,
                            "body": {
                                "message": "Duvida removida com sucesso",
                                "user": user
                            }
                        })
                        data.headers.add('Access-Control-Allow-Headers', '*')
                        data.headers.add('Access-Control-Allow-Origin', '*')
                        data.headers.add("Access-Control-Allow-Methods", ' *')
                        return data

            data = jsonify({
                'statusCode': 404,
                "body": {
                    "message": "Duvida não encontrada"
                }
            })
            data.headers.add('Access-Control-Allow-Headers', '*')
            data.headers.add('Access-Control-Allow-Origin', '*')
            data.headers.add("Access-Control-Allow-Methods", ' *')
            return data
