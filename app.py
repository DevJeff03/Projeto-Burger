from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from urllib.parse import unquote


from Models import Clientes, Hamburguer, Acompanhamentos, Bebidas, Sobremesas
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, methods=["GET", "HEAD", "POST", "OPTIONS", "PUT",
                                                                            "PATCH", "DELETE"], allow_headers=["*"],
     expose_headers=["Content-Type", "Authorization"], supports_credentials=True)


@app.before_request
def before_request():
    if request.method == "OPTIONS":
        # Adicione os cabeçalhos CORS necessários para a resposta OPTIONS
        headers = {
            "Access-Control-Allow-Origin": "http://localhost:4200",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Credentials": "true",
        }
        return jsonify({}), 200, headers

app.config['JWT_SECRET_KEY'] = 'teste123'
jwt = JWTManager(app)


class Cliente(Resource):
    def get(self, email):
        cliente = Clientes.query.filter_by(email=email).first()
        if cliente:
            response = {
                'id': cliente.idCliente,
                'nome': cliente.nome,
                'endereco': cliente.endereco,
                'telefone': cliente.telefone,
                'email': cliente.email,
                'foto_url': cliente.foto_url,
                'senha': cliente.senha,
                'tipo': cliente.tipo
            }
        else:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Cliente não encontrado.'
            }
        return response

    def put(self, nome):
        cliente = Clientes.query.filter_by(nome=nome).first()
        if cliente:
            try:
                dados = request.json
                if 'nome' in dados:
                    cliente.nome = dados['nome']
                if 'endereco' in dados:
                    cliente.endereco = dados['endereco']
                if 'telefone' in dados:
                    cliente.telefone = dados['telefone']
                if 'email' in dados:
                    cliente.email = dados['email']
                if 'foto_url' in dados:
                    cliente.foto_url = dados['foto_url']
                if 'senha' in dados:
                    cliente.senha = dados['senha']
                cliente.save()
                response = {
                    'id': cliente.idCliente,
                    'nome': cliente.nome,
                    'endereco': cliente.endereco,
                    'telefone': cliente.telefone,
                    'email': cliente.email,
                    'foto_url': cliente.foto_url,
                    'senha': cliente.senha,
                    'tipo': cliente.tipo
                }
            except AttributeError:
                response = {
                    'status': 'erro',
                    'mensagem': 'Erro ao atualizar cliente'
                }
        else:
            response = {
                'status': 'erro',
                'mensagem': 'Cliente não encontrado'
            }
        return response

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


class Lista_Cliente(Resource):
    def get(self):
        clientes = Clientes.query.all()
        response = [
            {
                'id': i.idCliente,
                'nome': i.nome,
                'endereco': i.endereco,
                'telefone': i.telefone,
                'email': i.email,
                'foto_url': i.foto_url,
                'senha': i.senha,
                'tipo': i.tipo
            } for i in clientes]
        return response


    def post(self):
        dados = request.json
        cliente = Clientes(nome=dados['nome'], endereco=dados['endereco'], telefone=dados['telefone'],
                           email=dados['email'], foto_url=dados['foto_url'], tipo=dados['tipo'], senha=dados['senha'])
        cliente.save()
        response = {
            'id': cliente.idCliente,
            'nome': cliente.nome,
            'endereço': cliente.endereco,
            'telefone': cliente.telefone,
            'email': cliente.email,
            'foto_url': cliente.foto_url,
            'tipo': cliente.tipo,
            'senha': cliente.senha
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
                'preco': hamburguer.preco,
                'imagem_url': hamburguer.imagem_url
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Hamburguer não encontrado.'
            }
        return response

    def put(self, ident):
        hamburguer = Hamburguer.query.filter_by(idHamburguer=ident).first()
        try:
            dados = request.json
            if 'nome' in dados:
                hamburguer.nome = dados['nome']
            if 'ingredientes' in dados:
                hamburguer.ingredientes = dados['ingredientes']
            if 'preco' in dados:
                hamburguer.preco = dados['preco']
            if 'imagem_url' in dados:
                hamburguer.imagem_url = dados['imagem_url']
            hamburguer.save()
            response = {
                'id': hamburguer.idHamburguer,
                'nome': hamburguer.nome,
                'ingredientes': hamburguer.ingredientes,
                'preco': hamburguer.preco,
                'imagem_url': hamburguer.imagem_url
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Hamburguer não encontrado'
            }
        return response

    def delete(self, ident):
        hamburguer = Hamburguer.query.filter_by(idHamburguer=ident).first()
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
        response = [{'id': i.idHamburguer, 'nome': i.nome, 'ingredientes': i.ingredientes, 'preco': i.preco,
                     'imagem_url': i.imagem_url} for i in hamburgueres]
        return response


    def post(self):
        dados = request.json
        hamburguer = Hamburguer(nome=dados['nome'], ingredientes=dados['ingredientes'], preco=dados['preco'],
                                imagem_url=dados['imagem_url'])
        hamburguer.save()
        response = {
            'id': hamburguer.idHamburguer,
            'nome': hamburguer.nome,
            'ingredientes': hamburguer.ingredientes,
            'preco': hamburguer.preco,
            'imagem_url': hamburguer.imagem_url
        }
        return response


class Bebida(Resource):
    def get(self, nome):
        bebida = Bebidas.query.filter_by(nome=nome).first()
        try:
            response = {
                'id': bebida.idBebida,
                'nome': bebida.nome,
                'fabricante': bebida.fabricante,
                'preco': bebida.preco,
                'imagem_url': bebida.imagem_url
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Bebida não encontrada.'
            }
        return response

    def put(self, ident):
        bebida = Bebidas.query.filter_by(idBebida=ident).first()
        try:
            dados = request.json
            if 'nome' in dados:
                bebida.nome = dados['nome']
            if 'fabricante' in dados:
                bebida.fabricante = dados['fabricante']
            if 'preco' in dados:
                bebida.preco = dados['preco']
            if 'imagem_url' in dados:
                bebida.imagem_url = dados['imagem_url']
            bebida.save()
            response = {
                'id': bebida.idBebida,
                'nome': bebida.nome,
                'fabricante': bebida.fabricante,
                'preco': bebida.preco,
                'imagem_url': bebida.imagem_url
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Bebida não encontrada'
            }
        return response

    def delete(self, ident):
        bebida = Bebidas.query.filter_by(idBebida=ident).first()
        try:
            mensagem = 'Bebida {} excluida com sucesso'.format(bebida.nome)
            bebida.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Bebida não encontrada'
            }
        return response


class Lista_Bebidas(Resource):
    def get(self):
        bebida = Bebidas.query.all()
        response = [{'id': i.idBebida, 'nome': i.nome, 'fabricante': i.fabricante, 'preco': i.preco,
                     'imagem_url': i.imagem_url} for i in bebida]
        return response

    def post(self):
        dados = request.json
        bebida = Bebidas(nome=dados['nome'], fabricante=dados['fabricante'], preco=dados['preco'],
                         imagem_url=dados['imagem_url'])
        bebida.save()
        response = {
            'id': bebida.idBebida,
            'nome': bebida.nome,
            'fabricante': bebida.fabricante,
            'preco': bebida.preco,
            'imagem_url': bebida.imagem_url
        }
        return response


class Acompanhamento(Resource):
    def get(self, nome):
        acompanhamento = Acompanhamentos.query.filter_by(nome=nome).first()
        try:
            response = {
                'id': acompanhamento.idAcompanhamento,
                'nome': acompanhamento.nome,
                'descricao': acompanhamento.descricao,
                'preco': acompanhamento.preco,
                'imagem_url': acompanhamento.imagem_url
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Acompanhamento não encontrado.'
            }
        return response

    def put(self, ident):
        acompanhamento = Acompanhamentos.query.filter_by(idAcompanhamento=ident).first()
        try:
            dados = request.json
            if 'nome' in dados:
                acompanhamento.nome = dados['nome']
            if 'descricao' in dados:
                acompanhamento.descricao = dados['descricao']
            if 'preco' in dados:
                acompanhamento.preco = dados['preco']
            if 'imagem_url' in dados:
                acompanhamento.imagem_url = dados['imagem_url']
            acompanhamento.save()
            response = {
                'id': acompanhamento.idAcompanhamento,
                'nome': acompanhamento.nome,
                'descricao': acompanhamento.descricao,
                'preco': acompanhamento.preco,
                'imagem_url': acompanhamento.imagem_url
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Acompanhamento não encontrado'
            }
        return response

    def delete(self, ident):
        acompanhamento = Acompanhamentos.query.filter_by(idAcompanhamento=ident).first()
        try:
            mensagem = 'Acompanhamento {} excluida com sucesso'.format(acompanhamento.nome)
            acompanhamento.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Acompanhamento não encontrado'
            }
        return response


class Lista_Acompanhamento(Resource):
    def get(self):
        acompanhamento = Acompanhamentos.query.all()
        response = [{'id': i.idAcompanhamento, 'nome': i.nome, 'descricao': i.descricao, 'preco': i.preco,
                     'imagem_url': i.imagem_url} for i in acompanhamento]
        return response

    def post(self):
        dados = request.json
        acompanhamento = Acompanhamentos(nome=dados['nome'], descricao=dados['descricao'], preco=dados['preco'],
                                         imagem_url=dados['imagem_url'])
        acompanhamento.save()
        response = {
            'id': acompanhamento.idAcompanhamento,
            'nome': acompanhamento.nome,
            'descricao': acompanhamento.descricao,
            'preco': acompanhamento.preco,
            'imagem_url': acompanhamento.imagem_url
        }
        return response


class Sobremesa(Resource):
    def get(self, nome):
        sobremesa = Sobremesas.query.filter_by(nome=nome).first()
        try:
            response = {
                'id': sobremesa.idSobremesa,
                'nome': sobremesa.nome,
                'descricao': sobremesa.descricao,
                'preco': sobremesa.preco,
                'imagem_url': sobremesa.imagem_url
            }
        except AttributeError:
            response = {
                'Status': 'Erro',
                'Mensagem': 'Sobremesa não encontrada.'
            }
        return response

    def put(self, ident):
        sobremesa = Sobremesas.query.filter_by(idSobremesa=ident).first()
        try:
            dados = request.json
            if 'nome' in dados:
                sobremesa.nome = dados['nome']
            if 'descricao' in dados:
                sobremesa.descricao = dados['descricao']
            if 'preco' in dados:
                sobremesa.preco = dados['preco']
            if 'imagem_url' in dados:
                sobremesa.imagem_url = dados['imagem_url']
            sobremesa.save()
            response = {
                'id': sobremesa.idSobremesa,
                'nome': sobremesa.nome,
                'descricao': sobremesa.descricao,
                'preco': sobremesa.preco,
                'imagem_url': sobremesa.imagem_url
            }
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Sobremesa não encontrada'
            }
        return response

    def delete(self, ident):
        sobremesa = Sobremesas.query.filter_by(idSobremesa=ident).first()
        try:
            mensagem = 'Sobremesa {} excluida com sucesso'.format(sobremesa.nome)
            sobremesa.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'erro',
                'mensagem': 'Sobremesa não encontrada'
            }
        return response


class Lista_Sobremesa(Resource):
    def get(self):
        sobremesa = Sobremesas.query.all()
        response = [{'id': i.idSobremesa, 'nome': i.nome, 'descricao': i.descricao, 'preco': i.preco,
                     'imagem_url': i.imagem_url} for i in sobremesa]
        return response

    def post(self):
        dados = request.json
        sobremesa = Sobremesas(nome=dados['nome'], descricao=dados['descricao'], preco=dados['preco'],
                               imagem_url=dados['imagem_url'])
        sobremesa.save()
        response = {
            'id': sobremesa.idSobremesa,
            'nome': sobremesa.nome,
            'descricao': sobremesa.descricao,
            'preco': sobremesa.preco,
            'imagem_url': sobremesa.imagem_url
        }
        return response


class Login(Resource):
    def post(self):
        dados = request.json
        email = dados.get('email')
        senha = dados.get('senha')

        if email and senha:
            cliente = Clientes.query.filter_by(email=email, senha=senha).first()

            if cliente:
                access_token = create_access_token(identity=cliente.idCliente)
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Credenciais inválidas'}, 401
        else:
            return {'message': 'Forneça email e senha'}, 400


api.add_resource(Cliente, '/cliente/<string:email>/')
api.add_resource(Lista_Cliente, '/clientes/')
api.add_resource(Hamburgueres, '/hamburguer/<string:ident>/')
api.add_resource(Lista_Hamburgueres, '/hamburgueres/')
api.add_resource(Bebida, '/bebida/<string:ident>/')
api.add_resource(Lista_Bebidas, '/bebidas/')
api.add_resource(Acompanhamento, '/acompanhamento/<string:ident>/')
api.add_resource(Lista_Acompanhamento, '/acompanhamentos/')
api.add_resource(Sobremesa, '/sobremesa/<string:ident>/')
api.add_resource(Lista_Sobremesa, '/sobremesas/')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
