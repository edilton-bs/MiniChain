import hashlib
import time

# Classe do Bloco
class Bloco:
    def __init__(self, indice, dados, hash_anterior):
        self.indice = indice
        self.timestamp = time.time()
        self.dados = dados
        self.hash_anterior = hash_anterior
        self.nonce = 0  # Será usado para mineração
        self.hash = self.calcular_hash()  # Calcula o hash ao criar o bloco

    def calcular_hash(self):
        # Combina as informações do bloco para gerar um hash
        conteudo = f"{self.indice}{self.timestamp}{self.dados}{self.hash_anterior}{self.nonce}"
        return hashlib.sha256(conteudo.encode()).hexdigest()

    def minerar_bloco(self, dificuldade):
        alvo = "0" * dificuldade  # Define o alvo com base na dificuldade
        while not self.hash.startswith(alvo):
            self.nonce += 1
            self.hash = self.calcular_hash()
        print(f"Bloco {self.indice} minerado! Nonce: {self.nonce}, Hash: {self.hash}")


# Classe da Blockchain
class Blockchain:
    def __init__(self):
        self.cadeia = [self.criar_bloco_genesis()]
        self.dificuldade = 4  # Define a dificuldade de mineração

    def criar_bloco_genesis(self):
        # Cria o bloco gênesis, o primeiro da cadeia
        return Bloco(0, "Bloco Gênesis", "0")

    def obter_ultimo_bloco(self):
        return self.cadeia[-1]

    def adicionar_bloco(self, dados):
        # Cria um novo bloco com o hash do último bloco
        novo_bloco = Bloco(len(self.cadeia), dados, self.obter_ultimo_bloco().hash)
        # Minera o bloco para que ele seja válido
        novo_bloco.minerar_bloco(self.dificuldade)
        self.cadeia.append(novo_bloco)

    def verificar_integridade(self):
        # Verifica a validade da blockchain inteira
        for i in range(1, len(self.cadeia)):
            bloco_atual = self.cadeia[i]
            bloco_anterior = self.cadeia[i - 1]

            # Verifica se o hash atual foi calculado corretamente
            if bloco_atual.hash != bloco_atual.calcular_hash():
                return False

            # Verifica se o hash anterior corresponde ao hash do bloco anterior
            if bloco_atual.hash_anterior != bloco_anterior.hash:
                return False
        return True
