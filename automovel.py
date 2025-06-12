from seguro import Seguro

class Automovel(Seguro):
    def __init__(self, cliente, modelo, ano, placa, cor, valor_segurado):
        super().__init__(cliente, tipo="Automóvel")
        self.modelo = modelo
        self.ano = int(ano)
        self.placa = placa
        self.cor = cor
        self.valor_segurado = valor_segurado
        self.valor_mensal = self.calcular_valor_mensal()

    def calcular_valor_mensal(self):
        if self.ano < 2010:
            return self.valor_segurado * 0.06
        elif self.ano <= 2018:
            return self.valor_segurado * 0.05
        else:
            return self.valor_segurado * 0.04

    def editar(self, modelo=None, ano=None, placa=None, cor=None, valor_segurado=None):
        if modelo is not None:
            self.modelo = modelo
        if ano is not None:
            self.ano = int(ano)
        if placa is not None:
            self.placa = placa
        if cor is not None:
            self.cor = cor
        if valor_segurado is not None:
            self.valor_segurado = valor_segurado
        self.valor_mensal = self.calcular_valor_mensal()

    def obter_valor_segurado(self):
        return self.valor_segurado

    def __str__(self):
        return (f"[Automóvel] Cliente: {self.cliente.nome}, Modelo: {self.modelo}, "
                f"Ano: {self.ano}, Placa: {self.placa}, Cor: {self.cor}, "
                f"Valor Segurado: R${self.valor_segurado:.2f}, Mensal: R${self.valor_mensal:.2f}, "
                f"Status: {'Ativo' if self.ativo else 'Cancelado'})")

def cadastrar_seguro(self):
    print("\n--- Cadastro de Seguro ---")
    cpf = input("CPF do cliente: ").strip()
    cliente = self.buscar_cliente(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    print("Tipos de seguro:")
    print("1. Automóvel")
    print("2. Residencial")
    print("3. Vida")
    tipo = input("Escolha o tipo de seguro (1/2/3): ")

    if tipo == "1":
        modelo = input("Modelo do veículo: ").strip()
        ano = input("Ano do veículo: ").strip()
        placa = input("Placa do veículo: ").strip()
        cor = input("Cor do veículo: ").strip()
        valor_segurado = Utils.ler_float("Valor segurado: R$ ")
        seguro = Automovel(cliente, modelo, ano, placa, cor, valor_segurado)
    elif tipo == "2":
        endereco = input("Endereço do imóvel: ").strip()
        cep = input("CEP: ").strip()
        valor = Utils.ler_float("Valor do imóvel: R$ ")
        seguro = Residencial(cliente, endereco, cep, valor)
    elif tipo == "3":
        valor_segurado = Utils.ler_float("Valor segurado: R$ ")
        beneficiarios = input("Beneficiários (separados por vírgula): ").strip().split(",")
        beneficiarios = [b.strip() for b in beneficiarios if b.strip()]
        seguro = Vida(cliente, valor_segurado, beneficiarios)
    else:
        print("Tipo de seguro inválido.")
        return

    seguro.valor_mensal = seguro.calcular_valor_mensal()
    self.seguros.append(seguro)
    self.salvar_dados()
    print("Seguro cadastrado com sucesso!")
    print(f"Número da apólice: {seguro.numero_apolice}")
