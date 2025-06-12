from seguro import Seguro

class Automovel(Seguro):
    def __init__(self, cliente, modelo, ano_carro, placa, cor, valor_segurado):
        super().__init__(cliente, tipo="Automóvel")
        self.modelo = modelo
        self.ano_carro = int(ano_carro)  # converte string para inteiro se necessário
        self.placa = placa
        self.cor = cor
        self.valor_segurado = valor_segurado
        self.valor_mensal = self.calcula_valor_mensal()

    def calcula_valor_mensal(self):
        if self.ano_carro < 2010:
            return self.valor_segurado * 0.06
        elif self.ano_carro <= 2018:
            return self.valor_segurado * 0.05
        else:
            return self.valor_segurado * 0.04

    def editar(self, modelo=None, ano_carro=None, placa=None, cor=None, valor_segurado=None):
        if modelo is not None:
            self.modelo = modelo
        if ano_carro is not None:
            self.ano_carro = int(ano_carro)
        if placa is not None:
            self.placa = placa
        if cor is not None:
            self.cor = cor
        if valor_segurado is not None:
            self.valor_segurado = valor_segurado
        self.valor_mensal = self.calcula_valor_mensal()

    def obter_valor_segurado(self):
        return self.valor_segurado

    def __str__(self):
        return (f"[Automóvel] Cliente: {self.cliente.nome}, Modelo: {self.modelo}, "
                f"Ano: {self.ano_carro}, Placa: {self.placa}, Cor: {self.cor}, "
                f"Valor Segurado: R${self.valor_segurado:.2f}, Mensal: R${self.valor_mensal:.2f}, "
                f"Status: {'Ativo' if self.ativo else 'Cancelado'}")
