from seguro import Seguro

class Residencial(Seguro):
    def __init__(self, cliente, endereco, cep, valor):
        super().__init__(cliente, tipo="Residencial")
        self.endereco = endereco
        self.cep = cep
        self.valor = float(valor)
        self.valor_mensal = self.calcula_valor_mensal()

    def calcula_valor_mensal(self):
        return round(self.valor * 0.0005, 2)

    def editar(self, endereco=None, cep=None, valor=None):
        if endereco:
            self.endereco = endereco
        if cep:
            self.cep = cep
        if valor:
            self.valor = valor
        self.valor_mensal = self.calcula_valor_mensal()

    def obter_valor_segurado(self):
        return self.valor
