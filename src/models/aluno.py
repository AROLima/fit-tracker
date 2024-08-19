from .protocolo_treinamento import ProtocoloTreinamento

class Aluno:
    def __init__(self, nome, idade, genero, protocolo_treinamento=None, id=None):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.genero = genero
        self.protocolo_treinamento = protocolo_treinamento

    def set_protocolo_treinamento(self, protocolo):
        if not isinstance(protocolo, ProtocoloTreinamento):
            raise ValueError("Protocolo de treinamento inválido")
        self.protocolo_treinamento = protocolo

    def calcular_imc(self, peso, altura):
        return peso / (altura ** 2)