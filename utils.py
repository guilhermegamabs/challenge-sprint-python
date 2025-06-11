import re
from datetime import datetime

class Utils:
    @staticmethod
    def validar_cpf(cpf):

        return cpf.isdigit() and len(cpf) == 11

    @staticmethod
    def formatar_data(data_str):

        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            return None

    @staticmethod
    def validar_email(email):

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None