class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco, telefone, email):
        self.nome = nome;
        self.cpf = cpf;
        self.data_nascimento = data_nascimento;
        self.endereco = endereco;
        self.telefone = telefone;
        self.email = email;
        
    def __str__(self):
        return f"Nome: {self.nome} | CPF: {self.cpf} | Email: {self.email} | Telefone: {self.telefone}"
    
    def editar(self, nome=None, data_nasc=None, endereco=None, telefone=None, email=None):
        if nome:
            self.nome = nome
        if data_nasc:
            self.data_nasc = data_nasc
        if endereco:
            self.endereco = endereco
        if telefone:
            self.telefone = telefone
        if email:
            self.email = email