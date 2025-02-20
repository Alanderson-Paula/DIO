import os

from colorama import Fore, Style, init

from conta_bancaria import ContaBancaria

# Inicializa o Colorama (necessário apenas no Windows)
init(autoreset=True)

# Criando uma instância da conta
conta = ContaBancaria()


def exibir_menu(opcao_selecionada=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('╔═════════════════════════════════════════════╗')
    print('║               BANCO D`PAULA                 ║')
    print('╚═════════════════════════════════════════════╝')
    print('╔═════════════════════════════════════════════╗')
    print('║        Selecione uma operação no menu       ║')
    print('╠═════════════════════════════════════════════╣')
    print(f'║ {(Fore.GREEN if opcao_selecionada == "1" else "")} {("✔" if opcao_selecionada == "1" else " ")}        1 - SAQUE{Style.RESET_ALL}                         ║')
    print(f'║ {(Fore.GREEN if opcao_selecionada == "2" else "")} {("✔" if opcao_selecionada == "2" else " ")}        2 - DEPÓSITO{Style.RESET_ALL}                      ║')
    print(f'║ {(Fore.GREEN if opcao_selecionada == "3" else "")} {("✔" if opcao_selecionada == "3" else " ")}        3 - EXTRATO{Style.RESET_ALL}                       ║')
    print(f'║ {(Fore.RED if opcao_selecionada == "4" else "")} {("✔" if opcao_selecionada == "4" else " ")}        4 - SAIR{Style.RESET_ALL}                          ║')
    print('╚═════════════════════════════════════════════╝')


exibir_menu()


def iniciar():
    while True:
        opcao = input('Selecione uma operação: ')
        exibir_menu(opcao)

        if opcao == '1':
            valor = float(input('Valor do Saque: '))
            if conta.sacar(valor):
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!\n")
        elif opcao == '2':
            valor = float(input('Informe o valor do depósito: '))
            dep = conta.depositar(valor)
            if dep is not None:
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\n")
        elif opcao == '3':
            conta.imprimir_extrato()
        elif opcao == '4':
            print("\nObrigado por usar o Banco D'Paula! Saindo...\n")
            break
        else:
            print("Opção inválida! Escolha novamente.\n")

        # input("Pressione Enter para continuar...")


if __name__ == "__main__":
    iniciar()


# # menu.py
# import os
# from colorama import Fore, Style, init
# from conta_bancaria import ContaBancaria

# # Inicializa o Colorama (necessário apenas no Windows)
# init(autoreset=True)

# # Criando uma instância da conta
# conta = ContaBancaria()

# def exibir_menu():
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print('╔═════════════════════════════════════════════╗')
#     print('║               BANCO D`PAULA                 ║')
#     print('╚═════════════════════════════════════════════╝')
#     print('╔═════════════════════════════════════════════╗')
#     print('║        Selecione uma operação no menu       ║')
#     print('╠═════════════════════════════════════════════╣')
#     print(f'║ {Fore.GREEN}✔      1 - SAQUE{Style.RESET_ALL}                            ║')
#     print(f'║ {Fore.GREEN}✔      2 - DEPÓSITO{Style.RESET_ALL}                         ║')
#     print(f'║ {Fore.GREEN}✔      3 - EXTRATO{Style.RESET_ALL}                          ║')
#     print(f'║ {Fore.RED}✔      4 - SAIR{Style.RESET_ALL}                             ║')
#     print('╚═════════════════════════════════════════════╝')

# def iniciar():
#     while True:
#         exibir_menu()
#         opcao = input('Selecione uma operação: ')

#         if opcao == '1':
#             valor = float(input('Valor do Saque: '))
#             if conta.sacar(valor):
#                 print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
#         elif opcao == '2':
#             valor = float(input('Informe o valor do depósito: '))
#             conta.depositar(valor)
#             print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
#         elif opcao == '3':
#             conta.imprimir_extrato()
#         elif opcao == '4':
#             print("Obrigado por usar o Banco D'Paula! Saindo...")
#             break
#         else:
#             print("Opção inválida! Escolha novamente.")

#         input("Pressione Enter para continuar...")

# if __name__ == "__main__":
#     iniciar()
