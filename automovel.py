from seguro import Seguro

class Automovel(Seguro):
    def __init__(self, cliente, modelo_carro, ano_carro, placa_carro, cor_carro, valor_segurado):
        super().__init__(cliente, tipo="Automóvel")
        self.modelo_carro = modelo_carro
        self.ano_carro = ano_carro
        self.placa_carro = placa_carro
        self.cor_carro = cor_carro
        self.valor_segurado = valor_segurado  
        self.valor_mensal = self.calcula_valor_mensal()
        
    def calcula_valor_mensal(self):
        if self.ano_carro < 2010:
            return 80.0
        elif self.ano_carro < 2020:
            return 100.0
        else:
            return 120.0      
         
    def editar(self, modelo=None, ano=None, placa=None, cor=None, valor_segurado=None):
        if modelo:
            self.modelo_carro = modelo
        if ano:
            self.ano_carro = ano
        if placa:
            self.placa_carro = placa
        if cor:
            self.cor_carro = cor 
        if valor_segurado is not None:
            self.valor_segurado = valor_segurado
        self.valor_mensal = self.calcula_valor_mensal()

    def obter_valor_segurado(self):
        return self.valor_segurado
