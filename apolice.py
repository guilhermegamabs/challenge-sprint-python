from datetime import datetime
import uuid

class Apolice:
    def __init__(self, tipo_seguro, cpf, dados):
        self.numero_apolice = self.gerar_numero()
        self.tipo = tipo_seguro
        self.cpf = cpf
        self.dados = dados
        self.valor_mensal = self.calcular_valor_mensal()
        self.created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    def gerar_numero(self):
        return str(uuid.uuid4())
    
    def calcular_valor_mensal(self):
        if self.tipo == "Residencial":
            return round(self.dados["valor"] * 0.0005, 2)
        elif self.tipo == "Vida":
            return round(self.dados["valor_segurado"] * 0.001, 2)
        elif self.tipo == "Automóvel":
            ano = self.dados['ano']
            if ano < 2010:
                return 80.00
            elif ano < 2020:
                return 100.00
            else:
                return 120.00
        return 0
    
    def exibir_resumo(self):
        return {
            "Número": self.numero_apolice,
            "Tipo": self.tipo,
            "CPF": self.cpf,
            "Valor mensal": self.valor_mensal,
            "Criado em": self.created_at
        }