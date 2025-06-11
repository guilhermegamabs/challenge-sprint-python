from cliente import Cliente
from automovel import Automovel
from residencial import Residencial
from vida import Vida
from sinistro import Sinistro

class SistemaSeguros:
    def __init__(self):
        self.clientes = {}
        self.seguros = []
        self.sinistros = [] 
        self.tipo_usuario = None
        self.usuarios = {
            "fiapadmin": ("fiapadmin2025", "admin"),
            "guilhermegama@fiap.com": ("rm565293", "user"),
            "guilhermeribeiro@fiap.com": ("rm561757", "user"),
            "carolinanovakc@fiap.com": ("rm565621", "user"),
            "felipeferraz@fiap.com": ("rm561451", "user")
        }

    def autenticar(self):
        print("=== LOGIN ===")
        usuario = input("Usuário: ")
        senha = input("Senha: ")

        if usuario in self.usuarios and self.usuarios[usuario][0] == senha:
            self.tipo_usuario = self.usuarios[usuario][1]
            print(f"Bem-vindo, {usuario} ({self.tipo_usuario})!")
            return True
        else:
            print("Usuário ou senha inválidos.")
            return False
    
    def menu(self):
        while True:
            print("\n===== SISTEMA DE SEGUROS =====")
            print("1. Cadastrar cliente")
            print("2. Cadastrar Seguro")
            print("3. Registrar Sinistro")
            print("4. Listar clientes")
            print("5. Listar seguros")
            print("6. Calcular Total de Prêmios Mensais")  
            print("7. Listar sinistros de um cliente")
            print("8. Listar Apólices Ativas")
            print("9. Editar Cliente")
            print("10. Editar Seguro")
            print("11. Editar Registro")
            print("12. Mudar Status Sinistro")
            print("13. Valor Total Segurado por Cliente")
            print("14. Apólices Emitidas por Tipo de Seguro")
            print("15. ")
            print("0. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else: 
                    self.cadastrar_cliente()
            elif opcao == "2":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else: 
                    self.cadastrar_seguro()
            elif opcao == "3":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else: 
                    self.registrar_sinistro()
            elif opcao == "4":
                self.listar_clientes()
            elif opcao == "5":
                self.listar_seguros()
            elif opcao == "6":
                self.calcular_total_premios_mensais()  
            elif opcao == "7":
                self.listar_sinistros_cliente()
            elif opcao == "8":
                self.listar_apolices_ativas()
            elif opcao == "9":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else:
                    self.editar_cliente()
            elif opcao == "10":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else:
                    self.editar_seguro()
            elif opcao == "11":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else:
                    self.editar_registro()
            elif opcao == "12":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else:
                    self.mudar_status_sinistro()       
            elif opcao == "13":
                cpf = input("Digite o CPF do cliente: ")
                self.calcular_valor_total_segurado_cliente(cpf)
            elif opcao == "14":
                self.listar_apolices_por_tipo()
            elif opcao == "0":
                print("\nEncerrando o sistema.")
                break
            else:
                print("\nOpção inválida.")

    def buscar_cliente(self, cpf):
        return self.clientes.get(cpf)
    
    def cadastrar_cliente(self):
        print("\n--- Cadastro de Cliente ---")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        if not self.validar_cpf(cpf):
            print("CPF inválido. Deve conter 11 dígitos.")
            return
        data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        cliente = Cliente(nome, cpf, data_nascimento, endereco, telefone, email)
        self.clientes[cpf] = cliente
        print("\nCliente cadastrado com sucesso!")
        
    def cadastrar_seguro(self):
        print("\n--- Cadastro de Seguro ---")
        cpf = input("CPF do cliente: ")
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("\nCliente não encontrado.")
            return

        print("\nTipos de seguro:")
        print("1. Automóvel")
        print("2. Vida")
        print("3. Residencial")
        tipo = input("\nEscolha o tipo de seguro: ")

        if tipo == "1":
            modelo = input("Modelo do carro: ")
            ano = int(input("Ano do carro: "))
            placa = input("Placa do carro: ")
            cor = input("Cor do carro: ")
            valor_segurado = float(input("Valor segurado do carro: "))  # novo input
            seguro = Automovel(cliente, modelo, ano, placa, cor, valor_segurado)
        elif tipo == "2":
            valor_segurado = float(input("Valor segurado: "))
            beneficiarios = input("Beneficiários (separados por vírgula): ").split(",")
            beneficiarios = [b.strip() for b in beneficiarios]
            seguro = Vida(cliente, valor_segurado, beneficiarios)
        elif tipo == "3":
            endereco = input("Endereço do imóvel: ")
            cep = input("CEP: ")
            valor = float(input("Valor do imóvel: "))
            seguro = Residencial(cliente, endereco, cep, valor)
        else:
            print("Tipo inválido.")
            return

        self.seguros.append(seguro)
        print(f"Seguro cadastrado com sucesso! Valor mensal: R$ {seguro.valor_mensal}")
        print(f"Número da Apólice: {seguro.numero_apolice}")

        
    def registrar_sinistro(self):
        print("\n--- Registrar Sinistro ---")
        cpf = input("CPF do cliente: ")
        numero_apolice = input("Número da apólice: ")

        apolice_valida = any(s.cliente.cpf == cpf and s.numero_apolice == numero_apolice for s in self.seguros)
        if not apolice_valida:
            print("Apólice ou CPF não encontrados.")
            return

        descricao = input("Descrição do sinistro: ")
        data_ocorrencia = input("Data do ocorrido (dd/mm/aaaa): ")
        sinistro = Sinistro(cpf, numero_apolice, descricao, data_ocorrencia)
        self.sinistros.append(sinistro)
        print("Sinistro registrado com sucesso.")

    def listar_clientes(self):
        print("\n--- Lista de Clientes ---")
        for cliente in self.clientes.values():
            print(f"Nome: {cliente.nome} | CPF: {cliente.cpf}")

    def listar_apolices_ativas(self):
        print("\n--- Apólices Ativas ---")
        if not self.seguros:
            print("Nenhuma apólice cadastrada.")
            return
        for seguro in self.seguros:
            print(f"Número: {seguro.numero_apolice} | Tipo: {seguro.tipo} | CPF: {seguro.cliente.cpf} | Valor mensal: R$ {seguro.valor_mensal}")

    def listar_seguros(self):
        print("\n--- Lista de Seguros ---")
        for seguro in self.seguros:
            print(f"Tipo: {seguro.tipo} | CPF: {seguro.cliente.cpf} | Apólice: {seguro.numero_apolice} | Valor mensal: R$ {seguro.valor_mensal}")

    def calcular_total_premios_mensais(self):
        total = sum(seguro.valor_mensal for seguro in self.seguros)
        print(f"\nTotal de prêmios mensais de todos os seguros: R$ {total:.2f}")

    def listar_sinistros_cliente(self):
        cpf = input("Digite o CPF do cliente: ")
        encontrados = [s for s in self.sinistros if s.cpf == cpf]
        
        if not encontrados:
            print("Nenhum sinistro encontrado para este CPF.")
            return
        
        print(f"\n--- Sinistros do cliente {cpf} ---")
        for sinistro in encontrados:
            print(f"Apólice: {sinistro.numero_apolice} | Descrição: {sinistro.descricao} | Data: {sinistro.data_ocorrencia} | Status: {sinistro.status}")

    def editar_cliente(self):
        cpf = input("Digite o CPF do cliente que deseja editar: ")
        cliente = self.clientes.get(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return

        print(f"Editando cliente {cliente.nome} (CPF: {cliente.cpf})")
        nome = input(f"Novo nome [{cliente.nome}]: ") or None
        data_nascimento = input(f"Nova data de nascimento [{cliente.data_nascimento}]: ") or None
        endereco = input(f"Novo endereço [{cliente.endereco}]: ") or None
        telefone = input(f"Novo telefone [{cliente.telefone}]: ") or None
        email = input(f"Novo email [{cliente.email}]: ") or None

        if nome:
            cliente.nome = nome
        if data_nascimento:
            cliente.data_nascimento = data_nascimento
        if endereco:
            cliente.endereco = endereco
        if telefone:
            cliente.telefone = telefone
        if email:
            cliente.email = email

        print("Cliente atualizado com sucesso.")

    def editar_seguro(self):
        numero_apolice = input("Digite o número da apólice que deseja editar: ")
        seguro = next((s for s in self.seguros if s.numero_apolice == numero_apolice), None)
        if not seguro:
            print("Apólice não encontrada.")
            return

        print(f"Editando apólice {numero_apolice} - Tipo: {seguro.tipo}")

        if seguro.tipo == "Automóvel":
            modelo = input(f"Novo modelo [{seguro.modelo_carro}]: ") or None
            ano = input(f"Novo ano [{seguro.ano_carro}]: ") or None
            placa = input(f"Nova placa [{seguro.placa_carro}]: ") or None
            cor = input(f"Nova cor [{seguro.cor_carro}]: ") or None
            valor_segurado = input(f"Novo valor segurado [{seguro.valor_segurado}]: ") or None
            ano = int(ano) if ano else None
            valor_segurado = float(valor_segurado) if valor_segurado else None
            seguro.editar(modelo, ano, placa, cor, valor_segurado)
        elif seguro.tipo == "Vida":
            valor_segurado = input(f"Novo valor segurado [{seguro.valor_segurado}]: ") or None
            beneficiarios = input(f"Novos beneficiários (separados por vírgula) [{', '.join(seguro.beneficiarios)}]: ") or None
            valor_segurado = float(valor_segurado) if valor_segurado else None
            beneficiarios = [b.strip() for b in beneficiarios.split(",")] if beneficiarios else None
            seguro.editar(valor_segurado, beneficiarios)
        elif seguro.tipo == "Residencial":
            endereco = input(f"Novo endereço [{seguro.endereco}]: ") or None
            cep = input(f"Novo CEP [{seguro.cep}]: ") or None
            valor = input(f"Novo valor do imóvel [{seguro.valor}]: ") or None
            valor = float(valor) if valor else None
            seguro.editar(endereco, cep, valor)
        else:
            print("Tipo de seguro inválido.")

        print("Seguro atualizado com sucesso.")


    def editar_registro(self):
        print("Funcionalidade ainda não implementada.")

    def mudar_status_sinistro(self):
        numero_apolice = input("Número da apólice do sinistro: ")
        sinistro = next((s for s in self.sinistros if s.numero_apolice == numero_apolice), None)
        if not sinistro:
            print("Sinistro não encontrado.")
            return
        novo_status = input(f"Novo status (Atual: {sinistro.status}): ")
        sinistro.status = novo_status
        print("Status do sinistro atualizado.")

    def calcular_valor_total_segurado_cliente(self, cpf):
        cliente = self.clientes.get(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        total = 0.0
        for seguro in self.seguros:
            if seguro.cliente.cpf == cpf:
                total += seguro.obter_valor_segurado()

        print(f"Valor total segurado do cliente {cliente.nome}: R$ {total:.2f}")

    def validar_cpf(self, cpf):
        return cpf.isdigit() and len(cpf) == 11

    def somente_admin(self):
        print("\nAcesso negado. Apenas usuários admin podem acessar esta função.")
        
    def listar_apolices_por_tipo(self):
        if not self.seguros:
            print("Nenhuma apólice cadastrada.")
            return

        contagem = {}
        for seguro in self.seguros:
            tipo = seguro.tipo
            contagem[tipo] = contagem.get(tipo, 0) + 1

        print("\n--- Apólices Emitidas por Tipo de Seguro ---")
        for tipo, quantidade in contagem.items():
            print(f"{tipo}: {quantidade} apólices")


if __name__ == "__main__":
    sistema = SistemaSeguros()
    if sistema.autenticar():
        sistema.menu()
