import socket
import threading
import csv
import json
import os
from flask import Flask, request, jsonify, send_from_directory, render_template

# Configurações
HOST = "0.0.0.0"
UDP_PORT = 5000
HTTP_PORT = 8000
RESULTS_FILE = "resultados.json"


# Variáveis globais
votos = {"a_favor": 0, "contra": 0, "abstencao": 0}
ids_votantes = set()
current_question = None


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('interface.html')

# Funções auxiliares
def salvar_resultados():
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "question": current_question,
            "results": votos,
            "ids_votantes": list(ids_votantes)
        }, f, ensure_ascii=False, indent=2)

def carregar_resultados():
    global votos, current_question, ids_votantes
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            votos = data.get("results", {"a_favor": 0, "contra": 0, "abstencao": 0})
            current_question = data.get("question")
            ids_votantes = set(data.get("ids_votantes", []))
    except FileNotFoundError:
        print("Arquivo JSON de resultados ainda não existe.")
        salvar_resultados()

# UDP Server
def handle_udp():
    global votos, ids_votantes
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind((HOST, UDP_PORT))
    print(f"[UDP] Servidor escutando em {HOST}:{UDP_PORT}")

    while True:
        data, addr = udp_server.recvfrom(1024)
        try:
            message = data.decode("utf-8")
            user_id, vote = message.split(":")

            if user_id in ids_votantes:
                udp_server.sendto("Erro: Você já votou.".encode("utf-8"), addr)
            elif vote in votos:
                votos[vote] += 1
                ids_votantes.add(user_id)
                salvar_resultados()
                udp_server.sendto("Voto registrado com sucesso!".encode("utf-8"), addr)
            else:
                udp_server.sendto("Erro: Opção de voto inválida.".encode("utf-8"), addr)
        except Exception as e:
            print(f"[UDP] Erro ao processar dados de {addr}: {e}")
            udp_server.sendto("Erro no processamento do voto.".encode("utf-8"), addr)

# Rotas HTTP

def index():
    return send_from_directory(os.getcwd(), "Interface.html")

@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.json
    senha = data.get("senha")
    if senha == "admin123":
        return jsonify({"auth": True})
    return jsonify({"auth": False}), 401

@app.route("/question", methods=["POST"])
def set_question():
    global current_question, votos, ids_votantes
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "Questão inválida"}), 400

    current_question = question
    votos = {"a_favor": 0, "contra": 0, "abstencao": 0}
    ids_votantes = set()
    salvar_resultados()
    print(f"[HTTP] Nova questão definida: {question}")
    return jsonify({"message": "Questão definida com sucesso."})

@app.route("/results", methods=["GET"])
def get_results():
    return jsonify({"question": current_question, "results": votos})

@app.route("/export", methods=["GET"])
def export_results():
    with open("resultados_votacao.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Opção", "Quantidade"])
        for opcao, qtd in votos.items():
            writer.writerow([opcao, qtd])
    return jsonify({"message": "Resultados exportados para CSV."})

@app.route("/vote", methods=["POST"])
def vote_http():
    global votos, ids_votantes
    data = request.json
    user_id = data.get("user_id")
    vote = data.get("vote")

    if not user_id or not vote:
        return jsonify({"error": "Dados inválidos"}), 400
    if user_id in ids_votantes:
        return jsonify({"error": "Você já votou."}), 400
    if vote not in votos:
        return jsonify({"error": "Opção de voto inválida."}), 400

    votos[vote] += 1
    ids_votantes.add(user_id)
    salvar_resultados()
    print(f"[HTTP] Voto registrado: {user_id} -> {vote}")
    return jsonify({"message": "Voto registrado com sucesso."})

@app.route("/json", methods=["GET"])
def get_json_file():
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            return f.read(), 200, {'Content-Type': 'application/json'}
    except FileNotFoundError:
        return jsonify({"error": "Arquivo não encontrado"}), 404

# Início do servidor
def main():
    carregar_resultados()
    threading.Thread(target=handle_udp, daemon=True).start()
    print(f"[HTTP] Servidor web iniciado em http://localhost:{HTTP_PORT}")
    app.run(host=HOST, port=HTTP_PORT)

if __name__ == "__main__":
    main()
