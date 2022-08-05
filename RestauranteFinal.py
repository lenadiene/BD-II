import pymongo
import certifi
client = pymongo.MongoClient(f"mongodb+srv://Esp:99ordep99@cluster0.p3zwv.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())

db = client['restaurante']
card = db['cardapio']
pedido = db['pedidos']
garcom = db['garcom']
mesa = db['mesa']

def menu():
    print("")
    print("=========== MENU ============")
    print("1 - Abrir Cardápio")
    print("2 - Editar pedido")
    print("3 - Deletar pedido")
    print("4 - Fechar Conta")
    print("5 - Adicionar item no cardapio")
    print("6 - Registrar garçom")
    print("7 - Registrar mesa")
    print("")
    ctrl = int(input("Selecione um item: "))
    if ctrl == 1:
        Cardapio()
    if ctrl == 2:
        nome = input("Digite o nome do cliente: ")
        editarpedido(nome)
    if ctrl == 3:
        nome = input("Digite o nome do cliente: ")
        cancelarpedido(nome)
    if ctrl == 4:
        nome = input("Digite o nome do cliente: ")
        finalizarpedido(nome)
    if ctrl == 5:
        adicionarItem()
    if ctrl == 6:
        registrargarcom()
    if ctrl == 7:
        registramesa()
    else:
        print("algo deu errado aí")

def Cardapio():
    print('CARDAPIO')
    for comida in card.find():
        print(comida.get('id'), "-", comida.get('Nome'), "-", comida.get('Valor'))

    gopedido = input("Deseja fazer pedido? (S/N)")
    if gopedido == "S":
        fazerpedido()
    else:
        menu()

def fazerpedido():
    listMesa = list()
    print("\n")
    print("#"*10)
    print("Mesas disponíveis:")
    for cMesa in mesa.find({'mesastatus': 'livre'}):
        print("Mesa: ", cMesa.get("numeromesa"))
        listMesa.append(cMesa.get("numeromesa"))
    if not listMesa:
        print("O restaurante está lotado no momento.")
        menu()
    else:

        select = list(map(int, input("selecione os itens:").strip().split()))
        nome = input("Digite o nome e sobrenome do cliente:")
        mesaN = int(input("Digite o número da mesa que o cliente vai sentar:"))
        listId = list()
        listGarcom = list()
        for cMesa in mesa.find({'numeromesa': int(mesaN)}):

                if cMesa.get("mesastatus") == "ocupado":
                    print("A mesa escolhida está ocupada no momento")
                    menu()
                else:
                    objeto_da_colecao = pedido.find_one({}, sort=[("id", -1)])
                    if not objeto_da_colecao:
                        id_anterior = 0
                    else:
                        id_anterior = objeto_da_colecao['id']

                    id_atual = int(id_anterior) + 1

                    print("Garçons disponíveis:")
                    for gar in garcom.find():
                        print('--------------------------------------')
                        print(gar.get('id'), "-", gar.get('Nome'))
                        listGarcom.append(gar.get('id'))
                        #print(listGarcom)
                    funcionario = int(input("Digite o id do Garçom: "))
                    if funcionario not in listGarcom:
                        print("Erro id do garçom não encontrado")
                        menu()
                    else:
                        for it in select:
                            for Lcomida in card.find({'id': int(it)}):
                                print("--------------------------------------")
                                print(Lcomida.get("Nome"), "-", Lcomida.get("Valor"))
                                listId.append(Lcomida.get("id"))
                                #print(listId)
                        if not listId:
                             menu()
                        else:
                            confirmar = input("Confirmar pedido (S/N)?")
                            if confirmar == "S":
                                itens = [
                                    {
                                        "id": id_atual,
                                        "nome": nome,
                                        "itens": listId,
                                        "contastatus": "pendente",
                                        "garcomId": funcionario,
                                        "mesacliente": mesaN,
                                        "totalpedidos": 0
                                    }
                                ]
                                amesa = {"$set": {"mesastatus": "ocupado"}}
                                mesa.update_one({"mesastatus": "livre", "numeromesa": int(mesaN)}, amesa)
                                pedido.insert_many(itens)

        #Simulação da impressão do pedido na cozinha
                                f = open("C:\\Users\\user\\OneDrive\\Documents\\IFPE\\2022.1\\banco de dados 2\\Trabalho de banco de dados 2\\pedidos.txt", "a")
                                f.write("=" * 20)
                                f.write("\n")
                                f.write(str(id_atual))
                                f.write("\n")
                                f.write(str("Nome do cliente:"))
                                f.write("\n")
                                f.write(nome)
                                f.write("\n")
                                f.write(str("Número da Mesa:"))
                                f.write("\n")
                                f.write(str(mesaN))
                                f.write("\n")
                                f.write(str("Itens do pedido:"))
                                f.write("\n")
                                for it in listId:
                                    for Lcomida in card.find({'id': int(it)}):
                                        f.write(Lcomida.get("Nome"))
                                        f.write("\n")
                                f.write("\n")
                                f.write(str("Garçom:"))
                                f.write("\n")
                                for func in garcom.find({'id': funcionario}):
                                    f.write(func.get("Nome"))
                                    f.write("\n")
                                f.write("=" * 20)
                                f.close()

                                # open and read the file after the appending:
                                f = open("pedidos.txt", "r")
                                for linha in f:
                                    linha = linha.rstrip()
                                    print(linha)
                                f.close()
                                print("Pedido concluido com sucesso!!!!!!")
                                menu()
                            else:
                                print("Pedido não concluido.")
                                menu()

def editarpedido(nome):
    listId = list()
    for meupedido in pedido.find({"nome": {'$regex': nome}}):
        print(meupedido.get('id'), "-", meupedido.get('nome'), "-", meupedido.get('contastatus'), "-",
              meupedido.get('itens'))
    ctrl = int(input("Selecione o cliente pelo seu id: "))

    for clientepedido in pedido.find({"id": int(ctrl)}):
        cstatus = clientepedido.get('contastatus')
        print(clientepedido.get('id'), "-", clientepedido.get('nome'), "-", clientepedido.get('contastatus'), "-",
              clientepedido.get('itens'))
        itens = clientepedido.get('itens')
        for it in itens:
            for Lcomida in card.find({'id': int(it)}):
                print("--------------------------------------")
                print(Lcomida.get('id'), "-", Lcomida.get("Nome"), "-", Lcomida.get("Valor"))
                print("")
        if cstatus == "fechado":
            print("O cliente selecionado já fechou a conta.")
            menu()
        else:
            for it in itens:
                for Lcomida in card.find({'id': int(it)}):

                    confirmar = input("Editar pedido (S/N)?")
                    print('CARDAPIO')
                    for comida in card.find():
                        print(comida.get('id'), "-", comida.get('Nome'), "-", comida.get('Valor'))
                    if confirmar == "S":
                        select = list(map(int, input("Selecione novos pedidos:").strip().split()))
                        for  itTwo in select:
                            for allcomida in card.find({'id': int(itTwo)}):
                                listId.append(allcomida.get("id"))
                                #print(listId)
                        if not listId:
                            print("Erro id de pedidos não encontrado")
                            menu()
                        else:
                            newvalues = {"$set": {"itens": listId}}
                            pedido.update_many({"itens": itens, "id": int(ctrl)}, newvalues)
                            print("Pedido alterado com sucesso !!!!!!")
                            menu()
                    else:
                        menu()
    menu()


def cancelarpedido(nome):
    for meupedido in pedido.find({"nome": {'$regex': nome}}):
        print(meupedido.get('id'), "-", meupedido.get('nome'), "-", meupedido.get('contastatus'), "-",
              meupedido.get('itens'))
    ctrl = int(input("Selecione o cliente pelo seu id: "))

    for clientepedido in pedido.find({"id": int(ctrl)}):
        cstatus = clientepedido.get('contastatus')
        itens = clientepedido.get('itens')
        mesaDoCliente = clientepedido.get('mesacliente')
        for it in itens:
            for Lcomida in card.find({'id': int(it)}):
                print("--------------------------------------")
                print(Lcomida.get('id'), "-", Lcomida.get("Nome"), "-", Lcomida.get("Valor"))
                print("")
        if cstatus == "fechado":
            print("O cliente mencionado já fechou a conta.")
            menu()
        else:

            confirmar = input("Cancelar pedido (S/N)?")
            if confirmar == "S":
                pedido.delete_one({"id": int(ctrl)})
                amesa = {"$set": {"mesastatus": "livre"}}
                mesa.update_one({"mesastatus": "ocupado", "numeromesa": int(mesaDoCliente)}, amesa)
                print("Pedido cancelado com sucesso !!!!!!")
                menu()
            else:
                menu()
    menu()


def finalizarpedido(nome):
    soma = 0
    for cliente in pedido.find({"nome": {'$regex': nome}}):
        print(cliente.get('id'), "-", cliente.get('nome'), "-", cliente.get('contastatus'), "-", cliente.get('itens'), "-", cliente.get('mesacliente'))
    ctrl = int(input("Selecione o cliente pelo seu id: "))
    for meupedido in pedido.find({"id": int(ctrl)}):
        itens = meupedido.get('itens')
        cstatus = meupedido.get('contastatus')
        mesaDoCliente = meupedido.get('mesacliente')
        # print(cstatus)
        if cstatus == "fechado":
            print("O cliente mencionado já fechou a conta.")
            menu()
        else:
            result = db.pedidos.aggregate([
                {"$match": {"id": ctrl}},
                {
                    '$lookup': {
                        'from': 'garcom',
                        'localField': 'garcomId',
                        'foreignField': 'id',
                        'as': 'Garçom'
                    },
                }, {'$unwind': '$Garçom'},
                {'$project': {'_id': 0, 'Garçom.Nome': 1}}

            ])

            for it in itens:
                for Lcomida in card.find({'id': int(it)}):
                    print("--------------------------------------")
                    print(Lcomida.get('id'), "-", Lcomida.get("Nome"), "-", Lcomida.get("Valor"))
                    print("")

                    soma += Lcomida.get("Valor")
            cstatus = {"$set": {"contastatus": "fechado"}}
            ctotal = {"$set": {"totalpedidos": soma}}
            pedido.update_one({"totalpedidos": 0, "id": int(ctrl)}, ctotal)
            pedido.update_one({"contastatus": "pendente", "id": int(ctrl)}, cstatus)
            amesa = {"$set": {"mesastatus": "livre"}}
            mesa.update_one({"mesastatus": "ocupado", "numeromesa": int(mesaDoCliente)}, amesa)
    for all in result:
        print("Garçom que atendeu: ", all)
        print("--------------------------------------")
    print("Valor de sua conta: ", "R$", soma)
    print("--------------------------------------")
    taxa = soma * 10 / 100
    print("Taxa de serviço do garçom: ", "R$", taxa)
    print("--------------------------------------")
    Vtotal = soma + taxa
    print("Valor total de sua conta:", "R$", Vtotal)
    print("--------------------------------------")
    pagar = input("Conta foi paga?(S/N) ")
    if pagar == "S":
        menu()
    else:
        menu()


def adicionarItem():
    print('CARDAPIO')
    for comida in card.find():
        print(comida.get('id'), "-", comida.get('Nome'), "-", comida.get('Valor'))
    print("--------------------------------------")
    # id = int(input("Digite o id do item: "))
    nome = input("Digite o nome do item: ")
    valor = int(input("Digite o valor do item: "))
    objeto_da_colecao = card.find_one({}, sort=[("id", -1)])
    if not objeto_da_colecao:
        id_anterior = 0
    else:
        id_anterior = objeto_da_colecao['id']

    id_atual = int(id_anterior) + 1
    data = [
        {"id": id_atual,
         "Nome": nome,
         "Valor": valor},
    ]
    card.insert_many(data)
    volta = input("Deseja adiconar mais itens? (S/N): ")
    if volta == "S":
        adicionarItem()
    else:
        menu()


def registrargarcom():
    for gar in garcom.find():
        print(gar.get('id'), "-", gar.get('Nome'))
    print("--------------------------------------")

    # id = int(input("Digite o id do garçom:"))
    nome = input("Digite o nome do garçom:")
    objeto_da_colecao = garcom.find_one({}, sort=[("id", -1)])
    if not objeto_da_colecao:
        id_anterior = 0
    else:
        id_anterior = objeto_da_colecao['id']

    id_atual = int(id_anterior) + 1
    data = [
        {"id": id_atual,
         "Nome": nome},
    ]
    garcom.insert_many(data)
    volta = input("Precisa registrar mais algum garçom? (S/N): ")
    if volta == "S":
        registrargarcom()
    else:
        menu()

    menu()
def registramesa():
    objeto_da_colecao = mesa.find_one({}, sort=[("numeromesa", -1)])
    if not objeto_da_colecao:
        id_anterior = 0
    else:
        id_anterior = objeto_da_colecao['numeromesa']

    id_atual = int(id_anterior) + 1
    data = [
        {"numeromesa": id_atual,
         "mesastatus": "livre"},
    ]
    mesa.insert_many(data)
    print("Mesa adicionada com sucesso!!!!!")
    volta = input("Precisa adicionar mais alguma mesa? (S/N): ")
    if volta == "S":
        registramesa()
    else:
        menu()

menu()