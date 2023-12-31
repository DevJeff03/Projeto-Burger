from flask import Flask, request
from flask_restful import Resource, Api
from Models import Clientes, Hamburguer, ItensPedido, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

@auth.verify_password
def verificacao(login, senha):
    if not(login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()



# Listar cliente individualmente
# Alterar dados de clientes já existentes
# Deletar clientes do BD
class Cliente(Resource):
    def get(self, nome):
        cliente = Clientes.query.filter_by(nome=nome).first()
        try:
            response = {
                'id': cliente.idCliente,
                'nome': cliente.nome,
                'endereco': cliente.endereco,
                'telefone': cliente.telefone,
                'email': cliente.email
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Cliente não encontrado.'
            }
        return response

    @auth.login_required
    def put(self, nome):
        cliente = Clientes.query.filter_by(nome=nome).first()
        try:
            dados = request.json
            if 'nome' in dados:
                cliente.nome = dados['nome']
            if 'endereco' in dados:
                cliente.endereco = dados['endereco']
            if 'telefone' in dados:
                cliente.telefone = dados['telefone']
            if 'telefone' in dados:
                cliente.email = dados['email']
            cliente.save()
            response = {
                'id': cliente.idCliente,
                'nome': cliente.nome,
                'endereco': cliente.endereco,
                'telefone': cliente.telefone,
                'email': cliente.email
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Cliente não encontrado'
            }
        return response

    @auth.login_required
    def delete(self, nome):
        cliente = Clientes.query.filter_by(nome=nome).first()
        try:
            mensagem = 'Cliente {} excluida(o) com sucesso'.format(cliente.nome)
            cliente.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Cliente não encontrado'
            }
        return response


# Listar Todos os Clientes
# Inserir clientes novos
class Lista_Cliente(Resource):
    def get(self):
        clientes = Clientes.query.all()
        response = [
            {'id': i.idCliente, 'nome': i.nome, 'endereco': i.endereco, 'telefone': i.telefone, 'email': i.email} for i
            in clientes]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        cliente = Clientes(nome=dados['nome'], endereco=dados['endereco'], telefone=dados['telefone'],
                           email=dados['email'])
        cliente.save()
        response = {
            'id': cliente.idCliente,
            'nome': cliente.nome,
            'endereço': cliente.endereco,
            'telefone': cliente.telefone,
            'email': cliente.email
        }
        return response


class Hamburgueres(Resource):
    def get(self, nome):
        hamburguer = Hamburguer.query.filter_by(nome=nome).first()
        try:
            response = {
                'id': hamburguer.idHamburguer,
                'nome': hamburguer.nome,
                'ingredientes': hamburguer.ingredientes,
                'preco': hamburguer.preco
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Hamburguer não encontrado.'
            }
        return response

    @auth.login_required
    def put(self, nome):
        hamburguer = Hamburguer.query.filter_by(nome=nome).first()
        try:
            dados = request.json
            if 'nome' in dados:
                hamburguer.nome = dados['nome']
            if 'ingredientes' in dados:
                hamburguer.ingredientes = dados['ingredientes']
            if 'preco' in dados:
                hamburguer.preco = dados['preco']
            hamburguer.save()
            response = {
                'id': hamburguer.idHamburguer,
                'nome': hamburguer.nome,
                'ingredientes': hamburguer.ingredientes,
                'preco': hamburguer.preco
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Hamburguer não encontrado'
            }
        return response

    @auth.login_required
    def delete(self, nome):
        hamburguer = Hamburguer.query.filter_by(nome=nome).first()
        try:
            mensagem = 'Hamburguer {} excluido com sucesso'.format(hamburguer.nome)
            hamburguer.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Hamburguer não encontrado'
            }
        return response


class Lista_Hamburgueres(Resource):
    def get(self):
        hamburgueres = Hamburguer.query.all()
        response = [{'id': i.idHamburguer, 'nome': i.nome, 'ingredientes': i.ingredientes, 'preco': i.preco} for i in
                    hamburgueres]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        hamburguer = Hamburguer(nome=dados['nome'], ingredientes=dados['ingredientes'], preco=dados['preco'])
        hamburguer.save()
        response = {
            'id': hamburguer.idHamburguer,
            'nome': hamburguer.nome,
            'ingredientes': hamburguer.ingredientes,
            'preco': hamburguer.preco
        }
        return response


class Itens(Resource):
    def get(self, descricao):
        item = ItensPedido.query.filter_by(descricao=descricao).first()
        try:
            response = {
                'id': item.idItem,
                'descricao': item.descricao,
                'fabricante': item.fabricante,
                'preco': item.preco
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Item não encontrado.'
            }
        return response

    @auth.login_required
    def put(self, descricao):
        item = ItensPedido.query.filter_by(descricao=descricao).first()
        try:
            dados = request.json
            if 'descricao' in dados:
                item.descricao = dados['descricao']
            if 'fabricante' in dados:
                item.fabricante = dados['fabricante']
            if 'preco' in dados:
                item.preco = dados['preco']
            item.save()
            response = {
                'id': item.idItem,
                'descricao': item.descricao,
                'fabricante': item.fabricante,
                'preco': item.preco
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Item não encontrado'
            }
        return response

    @auth.login_required
    def delete(self, descricao):
        item = ItensPedido.query.filter_by(descricao=descricao).first()
        try:
            mensagem = 'Item {} excluido com sucesso'.format(item.descricao)
            item.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Item não encontrado'
            }
        return response


class Lista_Itens(Resource):
    def get(self):
        itens = ItensPedido.query.all()
        response = [{'id': i.idItem, 'descricao': i.descricao, 'fabricante': i.fabricante, 'preco': i.preco} for i in
                    itens]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        item = ItensPedido(descricao=dados['descricao'], fabricante=dados['fabricante'], preco=dados['preco'])
        item.save()
        response = {
            'id': item.idItem,
            'descricao': item.descricao,
            'fabricante': item.fabricante,
            'preco': item.preco
        }
        return response






class Usuario(Resource):
    def get(self, login):
        usuario = Usuarios.query.filter_by(login=login).first()
        try:
            response = {
                'usuario': usuario.login,
                'senha': usuario.senha
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Usuario não encontrado.'
            }
        return response

    @auth.login_required
    def put(self, login):
        usuario = Usuarios.query.filter_by(login=login).first()
        try:
            dados = request.json
            if 'login' in dados:
                usuario.login = dados['login']
            if 'senha' in dados:
                usuario.senha = dados['senha']
            usuario.save()
            response = {
                'usuario': usuario.login,
                'senha': usuario.senha
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Usuario não encontrado'
            }
        return response

    @auth.login_required
    def delete(self, login):
        usuario = Usuarios.query.filter_by(login=login).first()
        try:
            mensagem = 'Usuario {} excluido com sucesso'.format(usuario.login)
            usuario.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Usuario não encontrado'
            }
        return response


class Lista_Usuarios(Resource):
    def get(self):
        usuarios = Usuarios.query.all()
        response = [{'login': i.login, 'senha': i.senha} for i in usuarios]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        usuario = Usuarios(login=dados['login'], senha=dados['senha'])
        usuario.save()
        response = {
                'usuario': usuario.login,
                'senha': usuario.senha
            }
        return response


api.add_resource(Cliente, '/cliente/<string:nome>/')
api.add_resource(Lista_Cliente, '/clientes/')
api.add_resource(Hamburgueres, '/hamburguer/<string:nome>/')
api.add_resource(Lista_Hamburgueres, '/hamburgueres/')
api.add_resource(Itens, '/item/<string:descricao>/')
api.add_resource(Lista_Itens, '/itens/')
api.add_resource(Usuario, '/usuario/<string:login>/')
api.add_resource(Lista_Usuarios, '/usuarios/')



if __name__ == '__main__':
    app.run(debug=True)
