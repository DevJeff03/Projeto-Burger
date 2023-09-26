from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func

# Criar BD
engine = create_engine('sqlite:///BestBurguer.db')
# Criar sessão para acesso ao Banco de Dados
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()




class Clientes(Base):
    __tablename__ = 'clientes'
    idCliente = Column(Integer, primary_key=True)
    nome = Column(String(50))
    endereco = Column(String(60))
    telefone = Column(Integer)
    email = Column(String(40))

    def __repr__(self):
        return f'<Cliente ID: {self.idCliente}, Nome: {self.nome}, ' \
               f'Endereço: {self.endereco}, Telefone: {self.telefone}, ' \
               f'Email: {self.email}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Hamburguer(Base):
    __tablename__ = 'hamburguer'
    idHamburguer = Column(Integer, primary_key=True)
    nome = Column(String(40))
    ingredientes = Column(String(200))
    preco = Column(Float)

    def __repr__(self):
        return f'<Hamburguer ID: {self.idHamburguer}, Nome: {self.nome}, ' \
               f'Ingredientes: {self.ingredientes}, Preço: {self.preco}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class ItensPedido(Base):
    __tablename__ = 'itens'
    idItem = Column(Integer, primary_key=True)
    descricao = Column(String(20))
    fabricante = Column(String(20))
    preco = Column(Float)

    def __repr__(self):
        return f'<Item Pedido ID: {self.idItem}, Descrição: {self.descricao}, ' \
               f'Fabricante: {self.fabricante}, Preço: {self.preco}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Pedidos(Base):
    __tablename__ = 'pedidos'
    idPedido = Column(Integer, primary_key=True)
    idCLiente = Column(Integer, ForeignKey('clientes.idCliente'))
    dataPedido = Column(DateTime, default=func.now())
    idHamburguer = Column(Integer, ForeignKey('hamburguer.idHamburguer'))
    itensPedido = Column(Integer, ForeignKey('itens.idItem'))
    tipoEntrega = Column(String(20))
    tipoPagamento = Column(String(20))
    cliente = relationship("Clientes")
    hamburguer = relationship("Hamburguer")
    itens = relationship("ItensPedido")


    def __repr__(self):
        # return '<Pedido {}>'.format(self.nome)
        return f'<Pedido ID: {self.idPedido}, Cliente: {self.idCliente}, ' \
               f'Data: {self.dataPedido}, Hambúrguer: {self.idHamburguer}, ' \
               f'Itens: {self.itensPedido}, Entrega: {self.tipoEntrega}, ' \
               f'Pagamento: {self.tipoPagamento}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
