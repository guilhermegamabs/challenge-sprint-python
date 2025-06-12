import uuid
from datetime import datetime

class Seguro:
    def __init__(self, cliente, tipo):
        self.cliente = cliente
        self.tipo = tipo
        self.data_inicio = datetime.now().strftime("%d/%m/%Y")
        self.ativo = True  


    def gerar_numero_apolice(self):
        import random
        return str(random.randint(10000, 99999))

    def obter_valor_segurado(self):
        raise NotImplementedError("Este método deve ser implementado na subclasse")
