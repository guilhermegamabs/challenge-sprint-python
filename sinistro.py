from datetime import datetime

class Sinistro:
    _sinistros = []
    def __init__(self, cpf, numero_apolice, descricao, data_ocorrencia):
        self.cpf = cpf
        self.numero_apolice = numero_apolice
        self.descricao = descricao
        self.data_ocorrencia = data_ocorrencia
        self.status = "Aberto"
        self.created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def exibir_detalhes(self):
        print(f"Apólice: {self.numero_apolice}")
        print(f"Descrição: {self.descricao}")
        print(f"Data do ocorrido: {self.data_ocorrencia}")
        print(f"Status: {self.status}")
        print(f"Registrado em: {self.created_at}")
        print("-" * 30)
        
    @classmethod
    def registrar(cls, cpf, numero_apolice, descricao, data_ocorrencia):
        sinistro = cls(cpf, numero_apolice, descricao, data_ocorrencia)
        cls._sinistros.append(sinistro)
        print(f"Sinistro registrado para CPF {cpf}, apólice {numero_apolice}.")

    @classmethod
    def listar_por_cliente(cls, cpf):
        encontrados = [s for s in cls._sinistros if s.cpf == cpf]
        if not encontrados:
            print(f"Nenhum sinistro encontrado para CPF {cpf}.")
            return

        print(f"\n=== Sinistros para CPF {cpf} ===")
        for sin in encontrados:
            sin.exibir_detalhes()

    def editar(self, descricao=None, data_ocorrencia=None):
        if descricao:
            self.descricao = descricao
        if data_ocorrencia:
            self.data_ocorrencia = data_ocorrencia

    def mudar_status(self, novo_status):
        self.status = novo_status