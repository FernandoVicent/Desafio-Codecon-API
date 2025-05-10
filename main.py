from flask import Flask, request, jsonify
from collections import Counter

import json
import time

from pydantic.v1.schema import json_scheme

app = Flask(__name__)

# Simulando um banco de dados em memória
usuarios_db = []

@app.route('/users', methods=['POST'])
def upload_arquivo_json():

    if 'file' not in request.files:
        return jsonify({'erro': 'Arquivo não enviado com o nome file'})

    arquivo = request.files['file']
    conteudo = json.load(arquivo)
    usuarios_db.extend(conteudo)

    return jsonify('usuários adicionados')


@app.route('/superusers', methods=['GET'])
def super_users():
    inicio = time.time()
    superusers = [
        usuario for usuario in usuarios_db
        if usuario.get('score') >= 900 and usuario.get('active') == True
    ]
    fim = time.time()
    tempo_processamento = round(fim - inicio, 4)
    resposta = {
        'total': len(superusers),
        'timeElapse': tempo_processamento,
        'user_list': superusers
    }
    return jsonify(resposta)

@app.route('/users', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios_db)

@app.route('/top-countries', methods=['GET'])
def top_countries():
    inicio = time.time()

    # Filtra superusuários
    superusers = [
        u for u in usuarios_db
        if u.get('score', 0) >= 900 and u.get('active') is True
    ]




if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)