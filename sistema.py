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
                    self.editar_sinistro()
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
        nome = input("Nome: ").strip()
        cpf = input("CPF (somente números): ").strip()
        data_nascimento_input = input("Data de nascimento (dd/mm/aaaa): ").strip()
        endereco = input("Endereço: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("Email: ").strip()

        if not Utils.validar_campos_obrigatorios(
            nome=nome, cpf=cpf, data_nascimento=data_nascimento_input, endereco=endereco, email=email
        ):
            print("Erro: Preencha todos os campos obrigatórios.")
            return

        if not Utils.validar_cpf(cpf):
            print("Erro: CPF inválido. Deve conter 11 dígitos e passar na validação.")
            return

        if not Utils.validar_data_nascimento(data_nascimento_input):
            print("Erro: Data de nascimento inválida ou cliente menor de 18 anos.")
            return

        if cpf in self.clientes:
            print("Erro: Cliente já cadastrado.")
            return
        
        novo_email = email.strip().lower()
        for c in self.clientes.values():
            if c.email.strip().lower() == novo_email and c.cpf != cpf:
                print("Email já cadastrado para outro cliente.")
                return

        data_nascimento = Utils.converter_data(data_nascimento_input)

        cliente = Cliente(nome, cpf, data_nascimento.strftime("%d/%m/%Y"), endereco, telefone, email)
        self.clientes[cpf] = cliente
        self.salvar_dados()
        print("Cliente cadastrado com sucesso!")

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

    def registrar_sinistro(self):
        print("\n--- Registrar Sinistro ---")
        cpf = input("CPF do cliente: ").strip()
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        numero_apolice = input("Número da apólice: ").strip()
        seguro = next((s for s in self.seguros if s.numero_apolice == numero_apolice), None)
        if not seguro:
            print("Apólice não encontrada.")
            return
        
        descricao = input("Descrição do sinistro: ").strip()
        data_ocorrencia = input("Data da ocorrência (dd/mm/aaaa): ").strip()

        if not Utils.converter_data(data_ocorrencia):
            print("Data inválida.")
            return
        
        sinistro = Sinistro(cpf, numero_apolice, descricao, data_ocorrencia)
        self.sinistros.append(sinistro)
        self.salvar_dados()
        print("Sinistro registrado com sucesso.")

    def listar_clientes(self):
        print("\n--- Lista de Clientes ---")
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return
        for cliente in self.clientes.values():
            print(f"Nome: {cliente.nome} | CPF: {cliente.cpf} | Email: {cliente.email} | Telefone: {cliente.telefone}")

    def listar_seguros(self):
        print("\n--- Lista de Seguros ---")
        if not self.seguros:
            print("Nenhum seguro cadastrado.")
            return
        for seguro in self.seguros:
            print(f"Apolice: {seguro.numero_apolice}, Tipo: {seguro.tipo}, Cliente: {seguro.cliente.nome}")

    def calcular_total_premios_mensais(self):
        total = sum(seguro.valor_mensal for seguro in self.seguros)
        print(f"\nTotal de prêmios mensais: R$ {total:.2f}")

    def listar_sinistros_cliente(self):
        cpf = input("Digite o CPF do cliente: ").strip()
        sinistros_cliente = [s for s in self.sinistros if s.cpf == cpf]
        if not sinistros_cliente:
            print("Nenhum sinistro encontrado para este cliente.")
            return
        print(f"\nSinistros para o cliente {cpf}:")
        for sinistro in sinistros_cliente:
            print(f"Nº Apólice: {sinistro.numero_apolice}, Descrição: {sinistro.descricao}, Data: {sinistro.data_ocorrencia}, Status: {sinistro.status}")

    def listar_apolices_ativas(self):
        print("\n--- Apólices Ativas ---")
        apolices_ativas = [s for s in self.seguros if s.ativo]
        if not apolices_ativas:
            print("Nenhuma apólice ativa encontrada.")
            return
        for seguro in apolices_ativas:
            print(f"Apolice: {seguro.numero_apolice}, Tipo: {seguro.tipo}, Cliente: {seguro.cliente.nome}")

    def alterar_contato_cliente(self):
        cpf = input("Digite o CPF do cliente a ser alterado: ").strip()
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        novo_endereco = input(f"Novo endereço (atual: {cliente.endereco}): ").strip()
        novo_telefone = input(f"Novo telefone (atual: {cliente.telefone}): ").strip()
        novo_email = input(f"Novo email (atual: {cliente.email}): ").strip()

        if novo_email:
            for c in self.clientes.values():
                if c.email.lower() == novo_email.lower() and c.cpf != cpf:
                    print("Email já cadastrado para outro cliente.")
                    return

        if novo_endereco:
            cliente.endereco = novo_endereco
        if novo_telefone:
            cliente.telefone = novo_telefone
        if novo_email:
            cliente.email = novo_email

        self.salvar_dados()
        print("Dados do cliente atualizados.")

    def editar_seguro(self):
        numero_apolice = input("Digite o número da apólice para editar: ").strip()
        seguro = next((s for s in self.seguros if s.numero_apolice == numero_apolice), None)
        if not seguro:
            print("Apólice não encontrada.")
            return

        if seguro.tipo == "Automóvel":
            modelo = input(f"Modelo ({seguro.modelo}): ").strip()
            ano = input(f"Ano ({seguro.ano}): ").strip()
            placa = input(f"Placa ({seguro.placa}): ").strip()
            cor = input(f"Cor ({seguro.cor}): ").strip()
            valor_segurado = input(f"Valor segurado (R$ {seguro.valor_segurado}): ").strip()

            if modelo:
                seguro.modelo = modelo
            if ano:
                try:
                    seguro.ano = int(ano)
                except ValueError:
                    print("Ano Inválido")
                    return
            if placa:
                seguro.placa = placa
            if cor:
                seguro.cor = cor
            if valor_segurado:
                try:
                    seguro.valor_segurado = float(valor_segurado)
                except ValueError:
                    print("Valor segurado inválido.")
                    return

        elif seguro.tipo == "Residencial":
            endereco = input(f"Endereço ({seguro.endereco}): ").strip()
            cep = input(f"CEP ({seguro.cep}): ").strip()
            valor = input(f"Valor do imóvel (R$ {seguro.valor}): ").strip()

            if endereco:
                seguro.endereco = endereco
            if cep:
                seguro.cep = cep
            if valor:
                try:
                    seguro.valor = float(valor)
                except ValueError:
                    print("Valor inválido.")
                    return

        elif seguro.tipo == "Vida":
            valor_segurado = input(f"Valor segurado (R$ {seguro.valor_segurado}): ").strip()
            beneficiarios = input(f"Beneficiários ({', '.join(seguro.beneficiarios)}): ").strip()

            if valor_segurado:
                try:
                    seguro.valor_segurado = float(valor_segurado)
                except ValueError:
                    print("Valor segurado inválido.")
                    return
            if beneficiarios:
                seguro.beneficiarios = [b.strip() for b in beneficiarios.split(",") if b.strip()]

        seguro.calcular_valor_mensal()
        self.salvar_dados()
        print("Seguro atualizado com sucesso.")

    def editar_sinistro(self):
        numero_sinistro = input("\nDigite o número do sinistro que deseja editar: ").strip()
        try:
            numero_sinistro = int(numero_sinistro)
        except ValueError:
            print("Número de sinistro inválido.")
            return

        sinistro = next((s for s in self.sinistros if s.numero == numero_sinistro), None)
        if not sinistro:
            print("Sinistro não encontrado.")
            return

        print(f"Editando sinistro número: {sinistro.numero}")
        print(f"\nCPF ({sinistro.cpf})")
        print(f"Apólice ({sinistro.numero_apolice})")
        descricao = input(f"Descrição ({sinistro.descricao}): ").strip()
        data_ocorrencia = input(f"Data do ocorrido ({sinistro.data_ocorrencia}): ").strip()

        sinistro.editar(
            descricao=descricao if descricao else None,
            data_ocorrencia=data_ocorrencia if data_ocorrencia else None
        )
        print("Sinistro atualizado com sucesso.")
    def mudar_status_sinistro(self):
        numero_apolice = input("Número da apólice: ").strip()
        sinistros = [s for s in self.sinistros if s.numero_apolice == numero_apolice]
        if not sinistros:
            print("Nenhum sinistro encontrado para essa apólice.")
            return
        print("Sinistros encontrados:")
        for idx, sinistro in enumerate(sinistros, 1):
            print(f"{idx}. {sinistro.descricao} - Status: {sinistro.status}")
        escolha = input("Escolha o número do sinistro para alterar o status: ")
        try:
            idx = int(escolha) - 1
            if idx < 0 or idx >= len(sinistros):
                print("Escolha inválida.")
                return
            novo_status = input("Novo status (Aberto/Em Análise/Fechado): ").strip()
            if novo_status not in ["Aberto", "Em Análise", "Fechado"]:
                print("Status inválido.")
                return
            sinistros[idx].status = novo_status
            self.salvar_dados()
            print("Status do sinistro atualizado.")
        except ValueError:
            print("Escolha inválida.")

    def calcular_valor_total_segurado_cliente(self, cpf):
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        total = sum(seguro.valor_segurado if hasattr(seguro, 'valor_segurado') else getattr(seguro, 'valor', 0) for seguro in self.seguros if seguro.cliente.cpf == cpf)
        print(f"Valor total segurado para o cliente {cliente.nome}: R$ {total:.2f}")

    def apolices_por_tipo(self):
        tipos = {}
        for seguro in self.seguros:
            tipos[seguro.tipo] = tipos.get(seguro.tipo, 0) + 1
        print("\nApólices emitidas por tipo:")
        for tipo, quantidade in tipos.items():
            print(f"{tipo}: {quantidade}")

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
        print("\nRanking de clientes com mais apólices:")
        for cpf, qtd in ranking_ordenado:
            cliente = self.clientes.get(cpf)
            if cliente:
                print(f"{cliente.nome} - {qtd} apólices")

    def cancelar_apolice(self):
        numero_apolice = input("Digite o número da apólice a cancelar: ").strip()
        seguro = next((s for s in self.seguros if s.numero_apolice == numero_apolice), None)
        if not seguro:
            print("Apólice não encontrada.")
            return
        if not seguro.ativo:
            print("Apólice já está cancelada.")
            return
        confirmar = input("Confirma cancelamento da apólice? (s/n): ").lower()
        if confirmar == 's':
            seguro.ativo = False
            self.salvar_dados()
            print("Apólice cancelada com sucesso.")
        else:
            print("Cancelamento abortado.")

    def somente_admin(self):
        print("Esta funcionalidade é restrita a administradores.")
