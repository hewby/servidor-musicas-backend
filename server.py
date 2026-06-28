from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

pedidos = []
excluidos = []

@app.route("/pedido", methods=["POST"])
def receber_pedido():
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    link = dados.get("link", "").strip()

    if not nome or not link:
        return jsonify({"mensagem": "Nome e link são obrigatórios."}), 400

    pedidos.append({
        "id": str(uuid.uuid4()),
        "nome": nome,
        "link": link,
        "data": datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%H:%M:%S")
    })

    return jsonify({"mensagem": "Pedido recebido com sucesso."}), 200


@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    return jsonify(pedidos)


@app.route("/pedido/<pid>", methods=["DELETE"])
def deletar_pedido(pid):
    global pedidos, excluidos

    for p in pedidos:
        if p["id"] == pid:
            excluidos.append(p)
            break

    pedidos = [p for p in pedidos if p["id"] != pid]

    return jsonify({"mensagem": "Pedido movido para excluídos"}), 200


@app.route("/limpar_todos", methods=["POST"])
def limpar_todos():
    global pedidos
    pedidos.clear()
    return jsonify({"mensagem": "Todos os pedidos foram removidos."}), 200


@app.route("/limpar_invalidos", methods=["POST"])
def limpar_invalidos():
    return jsonify({"mensagem": "Sem inválidos (validação já feita no envio)."}), 200


@app.route("/excluidos", methods=["GET"])
def listar_excluidos():
    return jsonify(excluidos)


@app.route("/limpar_excluidos", methods=["POST"])
def limpar_excluidos():
    global excluidos
    excluidos.clear()
    return jsonify({"mensagem": "Histórico limpo"}), 200
    
