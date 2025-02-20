from datetime import datetime


class ContaBancaria:
    def __init__(self, saldo=0.0, limite=500, limite_saques=3):
        self.saldo = saldo
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0
        self.extrato = []

    def sacar(self, valor):
        if valor and self.saldo == 0.0:
            print(
                'Necessário realizar depósito, saldo em conta igual a R$ 0.0. Utilize a opção 2.')
            return False
        elif valor > self.saldo:
            print(
                f"Você não tem saldo suficiente. Saldo atual R$ {self.saldo:.2f}.")
            return False
        if valor > self.limite:
            print(
                f"Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f}.")
            return False
        if self.numero_saques >= self.limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False

        self.saldo -= valor
        self.extrato.append(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} => Saque: R$ {valor:.2f}")
        self.numero_saques += 1
        return True

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} => Depósito: R$ {valor:.2f}")
        else:
            print("Operação falhou! O valor informado é inválido.")
            return None

    def imprimir_extrato(self):
        print("\n================ EXTRATO ================\n")
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            print("\n".join(self.extrato))
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================\n")
