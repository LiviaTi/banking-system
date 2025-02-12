import textwrap


def menu():
    menu = """
    Digite o número da sua operação: 
    [1] Cadastrar usuário
    [2] Criar conta corrente
    [3] Depositar
    [4] Sacar
    [5] Extrato
    [6] Listar contas
    [0] Sair

    => """
    return int(input(textwrap.dedent(menu)))

def criar_usuario(usuarios):
    cpf = input("\nDigite o seu CPF:")
    usuario = filtrar_usuario(cpf,usuarios)

    if usuario:
        print("\n Já existe usuario com esse CPF!")
        return

    nome= input("Informe seu nome completo: ")
    data_nascimento = input("\nDigite sua data de nascimento (dd-mm-aaaa):")
    endereco = input("\nDigite seu endereço:")

    #adicionado como dicionário tupla
    usuarios.append({"nome":nome, "data_nascimento": data_nascimento, "cpf":cpf, "endereco": endereco})
    
    print("Usuário cadastrado com sucesso")

def filtrar_usuario(cpf,usuarios):
    usuarios_filtrados= [usuario for usuario in usuarios if usuario["cpf"]==cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    # [0] pq no maximo vai retornar um usuario só pq só existe 1 pessoa com o mesmo cpf

def criar_conta(agencia,numero_conta,usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf,usuarios)

    if usuario:
        print("\n Conta criada com sucesso")
        #agência e conta já vem por argumento então vinculo o usuário 
        #conta em formato dicionário
        #usuario armazena somente um valor pq ta vinculado a um unico cpf
        return {"agencia":agencia, "numero_conta":numero_conta,"usuario":usuario}
    
    print("\nUsuário não encontrado, criação de conta encerrada")

def listar_contas(contas):
    for conta in contas:
        linha= f"""\
            agencia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t {conta['usuario']['nome']}
        """
        print("\n")
        print("="*100)
        print(textwrap.dedent(linha))

    return
        
# O / significa que os argumentos só podem ser passados pela ordem correta, tudo o que está antes de / tem que ser passado por posição
def depositar(saldo,valor,extrato, /): 
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

# O * significa que os argumentos foram passados nomeados nome=valor
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= limite_saques

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso")

        else:
            print("Operação falhou! O valor informado é inválido.")

        return saldo, extrato

#/ vem de forma posicional * da frente vem de forma nominal nome=valor
def exibir_extrato(saldo,/,*,extrato):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")



def main():
    LIMITE_SAQUES = 3
    AGENCIA ="0001"

    numero_saques = 0
    extrato = ""
    saldo = 0
    limite = 500
    usuarios =[]
    contas =[]
    numero_conta=1

    while True:
        opcao = menu()

        if opcao==1:
            criar_usuario(usuarios)

        elif opcao==2:
            #len para contabilizar não depende de tentativas e sim do numero real de contas no dicionario
            # len +1 sempre inicia em 1, pq 0+1= 1 
            # ATENÇÃO: Se eu tivesse que excluir conta daria errado
            #numero_conta = len(contas)+1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                #esse contador é mais vantajoso pq caso conta excluida não tenho problema 
                numero_conta+=1

        elif opcao == 3:
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 4:
            valor = float(input("Informe o valor do saque: "))
            #Passagem por nome e valor
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == 5:
            exibir_extrato(saldo,extrato=extrato)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 0:
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()