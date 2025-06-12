import json
import os
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
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists("json/clientes.json"):
            with open("json/clientes.json", "r") as f:
                clientes_json = json.load(f)
                for cpf, dados in clientes_json.items():
                    cliente = Cliente(**dados)
                    self.clientes[cpf] = cliente

        if os.path.exists("json/seguros.json"):
            with open("json/seguros.json", "r") as f:
                seguros_json = json.load(f)
                for seguro_data in seguros_json:
                    tipo = seguro_data.get("tipo")
                    cliente_cpf = seguro_data.get("cliente_cpf")
                    cliente = self.clientes.get(cliente_cpf)
                    if not cliente:
                        continue
                    if tipo == "Automóvel":
                        seguro = Automovel(cliente, seguro_data["modelo"], seguro_data["ano"], seguro_data["placa"], seguro_data["cor"], seguro_data["valor_segurado"])
                    elif tipo == "Vida":
                        seguro = Vida(cliente, seguro_data["valor_segurado"], seguro_data["beneficiarios"])
                    elif tipo == "Residencial":
                        seguro = Residencial(cliente, seguro_data["endereco"], seguro_data["cep"], seguro_data["valor"])
                    else:
                        continue
                    seguro.numero_apolice = seguro_data["numero_apolice"]
                    seguro.valor_mensal = seguro_data["valor_mensal"]
                    self.seguros.append(seguro)

        if os.path.exists("json/sinistros.json"):
            with open("json/sinistros.json", "r") as f:
                sinistros_json = json.load(f)
                for sinistro_data in sinistros_json:
                    sinistro = Sinistro(
                        sinistro_data["cpf"],
                        sinistro_data["numero_apolice"],
                        sinistro_data["descricao"],
                        sinistro_data["data_ocorrencia"],
                        sinistro_data.get("status", "Aberto")
                    )
                    self.sinistros.append(sinistro)

    def salvar_dados(self):
        clientes_json = {cpf: cliente.__dict__ for cpf, cliente in self.clientes.items()}
        with open("json/clientes.json", "w") as f:
            json.dump(clientes_json, f, indent=4)

        seguros_json = []
        for seguro in self.seguros:
            if seguro.tipo == "Automóvel":
                dados = {
                    "tipo": seguro.tipo,
                    "cliente_cpf": seguro.cliente.cpf,
                    "numero_apolice": seguro.numero_apolice,
                    "modelo": seguro.modelo,
                    "ano": seguro.ano,
                    "placa": seguro.placa,
                    "cor": seguro.cor,
                    "valor_segurado": seguro.valor_segurado,
                    "valor_mensal": seguro.valor_mensal
                }
            elif seguro.tipo == "Vida":
                dados = {
                    "tipo": seguro.tipo,
                    "cliente_cpf": seguro.cliente.cpf,
                    "numero_apolice": seguro.numero_apolice,
                    "valor_segurado": seguro.valor_segurado,
                    "beneficiarios": seguro.beneficiarios,
                    "valor_mensal": seguro.valor_mensal
                }
            elif seguro.tipo == "Residencial":
                dados = {
                    "tipo": seguro.tipo,
                    "cliente_cpf": seguro.cliente.cpf,
                    "numero_apolice": seguro.numero_apolice,
                    "endereco": seguro.endereco,
                    "cep": seguro.cep,
                    "valor": seguro.valor,
                    "valor_mensal": seguro.valor_mensal
                }
            else:
                continue
            seguros_json.append(dados)
        with open("json/seguros.json", "w") as f:
            json.dump(seguros_json, f, indent=4)

        sinistros_json = [sinistro.__dict__ for sinistro in self.sinistros]
        with open("json/sinistros.json", "w") as f:
            json.dump(sinistros_json, f, indent=4)

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
                self.salvar_dados()
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
        try:
            data_nascimento = Utils.converter_data(data_nascimento_input)
        except ValueError:
            print("Data inválida.")
            return
        if cpf in self.clientes:
            print("Cliente já cadastrado.")
            return
        endereco = input("Endereço: ")
        email = input("Email: ")
        telefone = input("Telefone: ")
        cliente = Cliente(nome, cpf, data_nascimento.strftime("%d/%m/%Y"), endereco, email, telefone)
        self.clientes[cpf] = cliente
        print("Cliente cadastrado com sucesso!")

    def cadastrar_seguro(self):
        print("\n--- Cadastro de Seguro ---")
        print("Tipos de seguro disponíveis: 1 - Automóvel, 2 - Residencial, 3 - Vida")
        tipo = input("Escolha o tipo: ")
        cpf = input("CPF do cliente: ")
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return

        if tipo == "1":
            modelo = input("Modelo do carro: ")
            ano = input("Ano do carro: ")
            placa = input("Placa: ")
            cor = input("Cor: ")
            valor_segurado = float(input("Valor segurado: "))
            seguro = Automovel(cliente, modelo, ano, placa, cor, valor_segurado)
        elif tipo == "2":
            endereco = input("Endereço: ")
            cep = input("CEP: ")
            valor = float(input("Valor do imóvel: "))
            seguro = Residencial(cliente, endereco, cep, valor)
        elif tipo == "3":
            valor_segurado = float(input("Valor segurado: "))
            beneficiarios = input("Beneficiários (separados por vírgula): ").split(",")
            beneficiarios = [b.strip() for b in beneficiarios]
            seguro = Vida(cliente, valor_segurado, beneficiarios)
        else:
            print("Tipo inválido.")
            return
        self.seguros.append(seguro)
        print(f"Seguro {seguro.tipo} cadastrado com sucesso!")

    def registrar_sinistro(self):
        print("\n--- Registro de Sinistro ---")
        cpf = input("CPF do cliente: ")
        numero_apolice = input("Número da apólice: ")
        descricao = input("Descrição do sinistro: ")
        data_ocorrencia = input("Data da ocorrência (dd/mm/aaaa): ")
        sinistro = Sinistro(cpf, numero_apolice, descricao, data_ocorrencia)
        self.sinistros.append(sinistro)
        print("Sinistro registrado com sucesso!")

    def listar_clientes(self):
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return
        for cliente in self.clientes.values():
            print(cliente)

    def listar_seguros(self):
        if not self.seguros:
            print("Nenhum seguro cadastrado.")
            return
        for seguro in self.seguros:
            print(seguro)

    def calcular_total_premios_mensais(self):
        total = sum(seguro.valor_mensal for seguro in self.seguros)
        print(f"Total de prêmios mensais: R$ {total:.2f}")

    def listar_sinistros_cliente(self):
        cpf = input("Digite o CPF do cliente: ")
        sinistros_cliente = [s for s in self.sinistros if s.cpf == cpf]
        if not sinistros_cliente:
            print("Nenhum sinistro encontrado para este cliente.")
            return
        for sinistro in sinistros_cliente:
            print(sinistro)

    def listar_apolices_ativas(self):
        for seguro in self.seguros:
            print(f"Apolice: {seguro.numero_apolice} - Tipo: {seguro.tipo} - Cliente: {seguro.cliente.nome}")

    def alterar_contato_cliente(self):
        cpf = input("Digite o CPF do cliente para alterar contato: ")
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        email = input("Novo email: ")
        telefone = input("Novo telefone: ")
        cliente.email = email
        cliente.telefone = telefone
        print("Contato atualizado com sucesso.")

    def editar_seguro(self):
        numero = input("Número da apólice: ")
        seguro = next((s for s in self.seguros if s.numero_apolice == numero), None)
        if not seguro:
            print("Seguro não encontrado.")
            return
        if seguro.tipo == "Automóvel":
            modelo = input("Novo modelo do carro: ")
            seguro.modelo = modelo
        elif seguro.tipo == "Vida":
            valor_segurado = float(input("Novo valor segurado: "))
            seguro.valor_segurado = valor_segurado
        elif seguro.tipo == "Residencial":
            endereco = input("Novo endereço: ")
            seguro.endereco = endereco
        print("Seguro atualizado.")

    def editar_registro(self):
        print("Funcionalidade não implementada ainda.")

    def mudar_status_sinistro(self):
        numero_apolice = input("Número da apólice do sinistro: ")
        sinistro = next((s for s in self.sinistros if s.numero_apolice == numero_apolice), None)
        if not sinistro:
            print("Sinistro não encontrado.")
            return
        status = input("Novo status (Aberto/Fechado): ")
        if status not in ["Aberto", "Fechado"]:
            print("Status inválido.")
            return
        sinistro.status = status
        print("Status do sinistro atualizado.")

    def calcular_valor_total_segurado_cliente(self, cpf):
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        total = sum(seguro.valor_segurado if hasattr(seguro, "valor_segurado") else getattr(seguro, "valor", 0) for seguro in self.seguros if seguro.cliente.cpf == cpf)
        print(f"Valor total segurado para {cliente.nome}: R$ {total:.2f}")

    def apolices_por_tipo(self):
        tipos = {}
        for seguro in self.seguros:
            tipos[seguro.tipo] = tipos.get(seguro.tipo, 0) + 1
        for tipo, qtd in tipos.items():
            print(f"{tipo}: {qtd}")

    def quantidade_sinistros_abertos_fechados(self):
        abertos = sum(1 for s in self.sinistros if s.status == "Aberto")
        fechados = sum(1 for s in self.sinistros if s.status == "Fechado")
        print(f"Sinistros abertos: {abertos}")
        print(f"Sinistros fechados: {fechados}")

    def ranking_clientes_mais_apolices(self):
        ranking = {}
        for seguro in self.seguros:
            cpf = seguro.cliente.cpf
            ranking[cpf] = ranking.get(cpf, 0) + 1
        ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        print("Ranking de clientes com mais apólices:")
        for cpf, qtd in ranking_ordenado:
            cliente = self.buscar_cliente(cpf)
            print(f"{cliente.nome} - {qtd} apólices")

    def cancelar_apolice(self):
        numero = input("Número da apólice para cancelar: ")
        seguro = next((s for s in self.seguros if s.numero_apolice == numero), None)
        if not seguro:
            print("Apólice não encontrada.")
            return
        self.seguros.remove(seguro)
        print("Apólice cancelada.")

    def somente_admin(self):
        print("Acesso negado. Apenas administradores podem executar esta ação.")