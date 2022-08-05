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
    print("")
    print("Selecione 1 para abrir o Cardápio")
    print("")
    print("=============================")
    ctrl = int(input(" Digite 1: "))
    if ctrl == 1:
        Cardapio()


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
    print("\n")
    print("#" * 10)
    print("Mesas disponíveis:")
    for Mesa in mesa.find({'mesastatus': 'livre'}):
        print("Mesa: ", Mesa.get("numeromesa"))
    mesaN = int(input("Digite o número da mesa que deseja sentar:"))
    select = list(map(int, input("selecione o número dos itens que você deseja no cardápio :").strip().split()))
    nome = input("Digite seu nome e sobrenome: ")

    listId = list()
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
                # print('--------------------------------------')
                print(gar.get('id'), "-", gar.get('Nome'))
            funcionario = int(input("Digite o id do Garçom: "))
            for it in select:
                for Lcomida in card.find({'id': int(it)}):
                    print("--------------------------------------")
                    print(Lcomida.get("Nome"), "-", Lcomida.get("Valor"))
                    listId.append(Lcomida.get("id"))
                    print(listId)
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

                    # Simulação da impressão do pedido na cozinha
                    f = open("pedidos.txt", "a")
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
                    for it in select:
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

menu()