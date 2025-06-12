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
        self.ativo = True  

    def gerar_numero(self):
        return str(uuid.uuid4())

    def calcular_valor_mensal(self):
        if self.tipo == "Residencial":
            return round(self.dados.get("valor", 0) * 0.0005, 2)
        elif self.tipo == "Vida":
            return round(self.dados.get("valor_segurado", 0) * 0.001, 2)
        elif self.tipo == "Automóvel":
            ano = self.dados.get('ano', 0)
            if isinstance(ano, str) and ano.isdigit():
                ano = int(ano)
            if ano < 2010:
                return 80.00
            elif ano < 2020:
                return 100.00
            else:
                return 120.00
        return 0

    def cancelar(self):
        self.ativo = False

    def reativar(self):
        self.ativo = True

    def exibir_resumo(self):
        return {
            "Número": self.numero_apolice,
            "Tipo": self.tipo,
            "CPF": self.cpf,
            "Valor mensal": self.valor_mensal,
            "Criado em": self.created_at,
            "Status": "Ativo" if self.ativo else "Cancelado"
        }

    def __str__(self):
        status = "Ativo" if self.ativo else "Cancelado"
        return (f"Apólice Nº: {self.numero_apolice} | Tipo: {self.tipo} | CPF: {self.cpf} | "
                f"Valor Mensal: R$ {self.valor_mensal:.2f} | Criado em: {self.created_at} | Status: {status}")
