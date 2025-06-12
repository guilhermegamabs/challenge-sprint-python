from seguro import Seguro

class Residencial(Seguro):
    def __init__(self, cliente, endereco, cep, valor):
        super().__init__(cliente, tipo="Residencial")
        self.endereco = endereco
        self.cep = cep
        self.valor = float(valor)
        self.valor_mensal = self.calcular_valor_mensal()
    
    def __str__(self):
        return (f"[Residencial] Cliente: {self.cliente.nome}, Endereço: {self.endereco}, "
                f"Valor Segurado: R${self.valor:.2f}, Mensal: R${self.valor_mensal:.2f}, "
                f"Status: {'Ativo' if self.ativo else 'Cancelado'}")    

    def calcular_valor_mensal(self):
        return round(self.valor * 0.0005, 2)

    def editar(self, endereco=None, cep=None, valor=None):
        if endereco:
            self.endereco = endereco
        if cep:
            self.cep = cep
        if valor:
            self.valor = float(valor)
        self.valor_mensal = self.calcular_valor_mensal()

    def obter_valor_segurado(self):
        return self.valor
