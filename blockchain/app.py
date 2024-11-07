from flask import Flask, render_template, request, jsonify
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_blockchain', methods=['GET'])
def get_blockchain():
    # Converte cada bloco em um dicionário para facilitar o envio como JSON
    blockchain_data = [
        {
            "indice": bloco.indice,
            "dados": bloco.dados,
            "hash_anterior": bloco.hash_anterior,
            "hash": bloco.hash,
            "nonce": bloco.nonce,
            "timestamp": bloco.timestamp
        } for bloco in blockchain.cadeia
    ]
    return jsonify(blockchain_data)

@app.route('/criar_bloco_genesis', methods=['POST'])

@app.route('/adicionar_bloco', methods=['POST'])
def adicionar_bloco():
    dados = request.json['dados']
    blockchain.adicionar_bloco(dados)
    return jsonify({"success": True, "indice": len(blockchain.cadeia) - 1})

def repropagar_hashes(indice):
    """Recalcula e propaga hashes para todos os blocos a partir do índice fornecido."""
    for i in range(indice, len(blockchain.cadeia)):
        bloco_atual = blockchain.cadeia[i]
        bloco_atual.hash = bloco_atual.calcular_hash()  # Atualiza o hash do bloco atual

        # Atualiza o previous hash do próximo bloco, se existir
        if i + 1 < len(blockchain.cadeia):
            blockchain.cadeia[i + 1].hash_anterior = bloco_atual.hash

@app.route('/atualizar_dados', methods=['POST'])
def atualizar_dados():
    indice = int(request.json['indice'])
    dados = request.json['dados']
    blockchain.cadeia[indice].atualizar_dados(dados)
    repropagar_hashes(indice)
    return jsonify({"hash": blockchain.cadeia[indice].hash})

@app.route('/atualizar_nonce', methods=['POST'])
def atualizar_nonce():
    indice = int(request.json['indice'])
    nonce = int(request.json['nonce'])
    blockchain.cadeia[indice].atualizar_nonce(nonce)
    repropagar_hashes(indice)
    return jsonify({"hash": blockchain.cadeia[indice].hash})


@app.route('/minerar_bloco', methods=['POST'])
def minerar_bloco():
    indice = int(request.json['indice'])
    dificuldade = blockchain.dificuldade
    blockchain.cadeia[indice].minerar_bloco(dificuldade)
    repropagar_hashes(indice)
    return jsonify({"hash": blockchain.cadeia[indice].hash, "nonce": blockchain.cadeia[indice].nonce})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
