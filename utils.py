import re
from datetime import datetime, date

class Utils:
    @staticmethod
    def validar_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False

        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto

        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto

        return digito1 == int(cpf[9]) and digito2 == int(cpf[10])

    @staticmethod
    def formatar_data(data_str):
        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            return None

    @staticmethod
    def converter_data(data_str):
        # Retorna apenas a data (sem hora)
        try:
            return datetime.strptime(data_str, "%d/%m/%Y").date()
        except ValueError:
            return None

    @staticmethod
    def validar_data_nascimento(data_str):
        data = Utils.converter_data(data_str)
        if not data:
            return False
        hoje = date.today()
        if data >= hoje:
            return False
        idade = (hoje - data).days // 365
        if idade < 18:
            return False
        return True

    @staticmethod
    def validar_data_sinistro(data_str):
        data = Utils.converter_data(data_str)
        if not data:
            return False
        hoje = date.today()
        if data > hoje:
            return False
        return True

    @staticmethod
    def validar_campos_obrigatorios(**campos):
        for nome, valor in campos.items():
            if valor is None or (isinstance(valor, str) and valor.strip() == ""):
                print(f"O campo '{nome}' é obrigatório e não pode estar vazio.")
                return False
        return True

    @staticmethod
    def validar_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
