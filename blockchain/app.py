from flask import Flask, render_template, request, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()



@app.route('/')
def index():
    # Exibe o estado atual da blockchain
    return render_template('index.html', blockchain=blockchain.cadeia, valida=blockchain.verificar_integridade())

@app.route('/adicionar_bloco', methods=['POST'])
def adicionar_bloco():
    dados = request.form.get('dados')
    if dados:
        blockchain.adicionar_bloco(dados)
    return redirect(url_for('index'))

@app.route('/minerar_bloco', methods=['POST'])
def minerar_bloco():
    dificuldade = int(request.form.get('dificuldade', 4))
    bloco = blockchain.obter_ultimo_bloco()
    bloco.minerar_bloco(dificuldade)
    return redirect(url_for('index'))

@app.route('/validar_blockchain')
def validar_blockchain():
    valida = blockchain.verificar_integridade()
    return render_template('index.html', blockchain=blockchain.cadeia, valida=valida)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
