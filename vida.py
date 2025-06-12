from seguro import Seguro

class Vida(Seguro):
    def __init__(self, cliente, valor_segurado, beneficiarios):
        super().__init__(cliente, tipo="Vida")
        self.valor_segurado = valor_segurado
        self.beneficiarios = beneficiarios
        self.valor_mensal = self.calcula_valor_mensal()
        
    def __str__(self):
        return (f"[Vida] Cliente: {self.cliente.nome}, Valor Segurado: R${self.valor_segurado:.2f}, "
                f"Mensal: R${self.valor_mensal:.2f}, Beneficiários: {', '.join(self.beneficiarios)}, "
                f"Status: {'Ativo' if self.ativo else 'Cancelado'}")
        
    def calcula_valor_mensal(self):
        return self.valor_segurado * 0.02

    def editar(self, novo_valor_segurado=None, novos_beneficiarios=None):
        if novo_valor_segurado is not None:
            self.valor_segurado = novo_valor_segurado
        if novos_beneficiarios is not None:
            self.beneficiarios = novos_beneficiarios
        self.valor_mensal = self.calcula_valor_mensal()

    def obter_valor_segurado(self):
        return self.valor_segurado
