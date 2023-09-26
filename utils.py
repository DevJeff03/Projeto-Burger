from Models import Clientes, Hamburguer, ItensPedido, Pedidos

def insere_clientes():
    cliente = Clientes(nome='teste', endereco='Rua Voluntarios da Patria, 1234',telefone=11974108520,email='devison@dominio.com')
    print(cliente)
    cliente.save()

def consulta_clientes():
    clientes = Clientes.query.all()
    print(clientes)

def insere_hamburguer():
    hamburguer = Hamburguer(nome='TajMahal', ingredientes='ingredientes aqui', preco=17.50)
    print(hamburguer)


if __name__ == '__main__':
    #insere_hamburguer()
    insere_clientes()
    #consulta_clientes()