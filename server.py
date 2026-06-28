from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

pedidos = []

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
    "data": datetime.now().strftime("%H:%M:%S")
})

    return jsonify({"mensagem": "Pedido recebido com sucesso."}), 200

@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    return jsonify(pedidos)

@app.route("/pedido/<pid>", methods=["DELETE"])
def deletar_pedido(pid):
    global pedidos
    pedidos = [p for p in pedidos if p["id"] != pid]
    return jsonify({"mensagem": "Pedido removido."}), 200

@app.route("/limpar_todos", methods=["POST"])
def limpar_todos():
    global pedidos
    pedidos.clear()
    return jsonify({"mensagem": "Todos os pedidos foram removidos."}), 200

@app.route("/limpar_invalidos", methods=["POST"])
def limpar_invalidos():
    return jsonify({"mensagem": "Sem inválidos (validação já é feita no envio)."}), 200
    
