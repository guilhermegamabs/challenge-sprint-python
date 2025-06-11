from sistema import SistemaSeguros

def main():
    sistema = SistemaSeguros()
    if sistema.autenticar():
        sistema.menu()
    else:
        print("Falha na autenticação. Encerrando o programa.")

if __name__ == "__main__":
    main()
