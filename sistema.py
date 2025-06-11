from cliente import Cliente
from automovel import Automovel
from residencial import Residencial
from vida import Vida
from sinistro import Sinistro
from utils import Utils

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
            print("15. Quantidade de sinistros abertos/fechados")
            print("16. Ranking de clientes com mais apólices")
            print("17. Cancelar apólice")
            print("18. Atualizar status de sinistro")
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
                    self.alterar_contato_cliente()
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
                self.apolices_por_tipo()
            elif opcao == "15":
                self.quantidade_sinistros_abertos_fechados()
            elif opcao == "16":
                self.ranking_clientes_mais_apolices()
            elif opcao == "17":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else:
                    self.cancelar_apolice()
            elif opcao == "18":
                if self.tipo_usuario != "admin":
                    self.somente_admin()
                else:
                    self.mudar_status_sinistro()
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
        if not Utils.validar_cpf(cpf):
            print("CPF Inválido. Deve conter 11 dígitos (Sem traços e pontos)")
            return
        data_nascimento_input = input("Data de nascimento (dd/mm/aaaa): ")
        data_nascimento = Utils.formatar_data(data_nascimento_input)
        if not data_nascimento:
            print("Data de nascimento inválida!")
            return
        endereco = input("Endereço: ")
        telefone = input("Telefone (Sem parênteses ou traços): ")
        email = input("Email: ")
        if not Utils.validar_email(email):
            print("Email inválido!")
            return
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
            valor_segurado = float(input("Valor segurado: "))
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
            print(f"Nome: {cliente.nome} | CPF: {cliente.cpf} | Telefone: {cliente.telefone} | E-mail: {cliente.email}")

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

    def editar_seguro(self):
        numero_apolice = input("Digite o número da apólice: ")
        seguro = next((s for s in self.seguros if s.numero_apolice == numero_apolice), None)
        if not seguro:
            print("Apólice não encontrada.")
            return
        if seguro.tipo == "Automóvel":
            modelo = input(f"Modelo [{seguro.modelo}]: ") or seguro.modelo
            ano = input(f"Ano [{seguro.ano}]: ")
            ano = int(ano) if ano else seguro.ano
            placa = input(f"Placa [{seguro.placa}]: ") or seguro.placa
            cor = input(f"Cor [{seguro.cor}]: ") or seguro.cor
            seguro.modelo = modelo
            seguro.ano = ano
            seguro.placa = placa
            seguro.cor = cor
        elif seguro.tipo == "Vida":
            valor_segurado = input(f"Valor segurado [{seguro.valor_segurado}]: ")
            valor_segurado = float(valor_segurado) if valor_segurado else seguro.valor_segurado
            beneficiarios = input(f"Beneficiários (separados por vírgula) [{', '.join(seguro.beneficiarios)}]: ")
            beneficiarios = [b.strip() for b in beneficiarios.split(",")] if beneficiarios else seguro.beneficiarios
            seguro.valor_segurado = valor_segurado
            seguro.beneficiarios = beneficiarios
        elif seguro.tipo == "Residencial":
            endereco = input(f"Endereço [{seguro.endereco}]: ") or seguro.endereco
            cep = input(f"CEP [{seguro.cep}]: ") or seguro.cep
            valor = input(f"Valor do imóvel [{seguro.valor}]: ")
            valor = float(valor) if valor else seguro.valor
            seguro.endereco = endereco
            seguro.cep = cep
            seguro.valor = valor
        print("Seguro atualizado com sucesso.")

    def editar_registro(self):
        print("Funcionalidade ainda não implementada.")

    def mudar_status_sinistro(self):
        numero_apolice = input("Número da apólice do sinistro: ")
        sinistro = next((s for s in self.sinistros if s.numero_apolice == numero_apolice), None)
        if not sinistro:
            print("Sinistro não encontrado.")
            return
        print(f"Status atual: {sinistro.status}")
        novo_status = input("Novo status: ")
        confirmacao = input(f"Confirmar alteração do status para '{novo_status}'? (s/n): ").lower()
        if confirmacao == 's':
            sinistro.status = novo_status
            print("Status do sinistro atualizado.")
        else:
            print("Alteração de status cancelada.")

    def calcular_valor_total_segurado_cliente(self, cpf):
        seguros_cliente = [s for s in self.seguros if s.cliente.cpf == cpf]
        total = 0
        for seguro in seguros_cliente:
            if seguro.tipo == "Vida":
                total += seguro.valor_segurado
            elif seguro.tipo == "Residencial":
                total += seguro.valor
            elif seguro.tipo == "Automóvel":
                total += seguro.valor_mensal * 12
        print(f"Valor total segurado do cliente {cpf}: R$ {total:.2f}")

    def apolices_por_tipo(self):
        tipos = {"Automóvel": 0, "Vida": 0, "Residencial": 0}
        for seguro in self.seguros:
            if seguro.tipo in tipos:
                tipos[seguro.tipo] += 1
        print("\nApólices emitidas por tipo de seguro:")
        for tipo, quantidade in tipos.items():
            print(f"{tipo}: {quantidade}")

    def quantidade_sinistros_abertos_fechados(self):
        abertos = sum(1 for s in self.sinistros if s.status.lower() == "aberto")
        fechados = sum(1 for s in self.sinistros if s.status.lower() == "fechado")
        print(f"\nSinistros abertos: {abertos}")
        print(f"Sinistros fechados: {fechados}")

    def ranking_clientes_mais_apolices(self):
        contador = {}
        for seguro in self.seguros:
            cpf = seguro.cliente.cpf
            contador[cpf] = contador.get(cpf, 0) + 1
        ranking = sorted(contador.items(), key=lambda x: x[1], reverse=True)
        print("\nRanking de clientes com mais apólices:")
        for cpf, quantidade in ranking:
            cliente = self.clientes.get(cpf)
            nome = cliente.nome if cliente else "Desconhecido"
            print(f"{nome} (CPF: {cpf}) - {quantidade} apólices")

    def alterar_contato_cliente(self):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.clientes.get(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        telefone = input(f"Novo telefone [{cliente.telefone}] (Sem parênteses ou traços): ") or cliente.telefone
        email = input(f"Novo email [{cliente.email}]: ") or cliente.email
        if not Utils.validar_email(email):
            print("Email inválido.")
            return
        cliente.telefone = telefone
        cliente.email = email
        print("Dados de contato atualizados com sucesso.")

    def cancelar_apolice(self):
        numero_apolice = input("Digite o número da apólice que deseja cancelar: ")
        seguro = next((s for s in self.seguros if s.numero_apolice == numero_apolice), None)
        if not seguro:
            print("Apólice não encontrada.")
            return
        confirmacao = input(f"Tem certeza que deseja cancelar a apólice {numero_apolice}? (s/n): ").lower()
        if confirmacao == 's':
            self.seguros.remove(seguro)
            print("Apólice cancelada com sucesso.")
        else:
            print("Cancelamento abortado.")

    def somente_admin(self):
        print("Acesso permitido apenas para usuários administradores.")