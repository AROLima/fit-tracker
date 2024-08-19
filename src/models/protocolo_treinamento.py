from enum import Enum

class TipoProtocolo(Enum):
    EMAGRECIMENTO = "Emagrecimento"
    GANHO_MASSA = "Ganho de massa muscular"
    DEFINICAO = "Definição"

class ProtocoloTreinamento:
    def __init__(self, tipo, descricao=None):
        if not isinstance(tipo, TipoProtocolo):
            raise ValueError("Tipo de protocolo inválido")
        self.tipo = tipo
        self.descricao = descricao

    def __str__(self):
        return f"{self.tipo.value}: {self.descricao}" if self.descricao else self.tipo.value