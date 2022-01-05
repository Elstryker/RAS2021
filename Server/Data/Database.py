""" from Data.DataClasses import BetSlip,User,Event,Bet,Intervenor,Sport
from Data import DataBaseAccess
from Data.DataClasses.Sport import SportType """
from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Boolean, Float
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.util.langhelpers import memoized_instancemethod
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()

class Sport(Base):
    __tablename__ = "Desporto"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45))

class Intervenor_Event(Base):
    evento_id = Column("evento_id",Integer,ForeignKey('Evento.id'),primary_key=True)
    invervenor_id = Column("interveniente_id",Integer,ForeignKey('Interveniente.id'),primary_key=True)
    odd = Column("odd", Integer)

class Event(Base):
    __tablename__ = "Evento"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45))
    state = Column("estado", String(45))
    sport_id = Column("desporto_id", Integer,ForeignKey('Desporto.id'))
    sport = relationship(Sport, backref=backref("events", uselist=True))
    intervenors = relationship('Intervenor', secondary=intervenor_event, back_populates='events')

class Intervenor(Base):
    __tablename__ = "Interveniente"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45))
    events = relationship('Event', secondary=intervenor_event, back_populates='intervenors')


class User(Base):
    __tablename__ = 'Utilizador'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String(45), unique=True)
    username = Column("nome", String(45))
    password = Column("password", String(45))
    wallet = Column("saldo",Float)
    messages = Column("mensagens", String(2000))
    #wallet = newCurrenciesDict(currencies)
    birthDate = Column("data_nascimento", Date)

class BetSlip(Base):
    __tablename__ = "Boletim"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("utilizador_id", Integer,ForeignKey('Utilizador.id'))
    user = relationship(User, backref=backref('betslips', uselist=True))
    amount = Column("montante",Float)
    winValue = Column("valor_vitoria",Float)
    won = Column("acertou",Boolean)


""" class DataBase(DataBaseAccess.DataBaseAccess): """
class DataBase():

    def __init__(self) -> None:
        self.engine = create_engine("mysql://admin:password@localhost/rasbetDB", connect_args= dict(host='localhost', port=3306))
        self.session = Session(self.engine)
        if not database_exists(self.engine.url):
            print("Creating database")
            create_database(self.engine.url)
        print("Creating tables")
        Base.metadata.create_all(self.engine)

    def addUser(self, user: User):
        try:
            self.session.add(user)    
            self.session.commit() 
            print("Added user " + new_user.username)
        except:
            print("Erro na inserção de User")
            self.session.rollback()
        

    def addBetSlip(self, new_betslip: BetSlip):
        try:
            self.session.add(new_betslip)
            print("Added betslip " + str(new_betslip.winValue))
        except:
            print("Erro na inserção de Betslip")
            self.session.rollback()
        self.session.commit()        
        

    def getUser(self, user_id: Integer) -> User:
        user = self.session.query(User).filter(User.id == user_id).one()
        print(user.email)
        return user
        
    def getUserBetslips(self, user_id: Integer):
        betslips = self.session.query(BetSlip).filter(BetSlip.user_id == user_id).all()
        print("Getting user id " + str(user_id) + " betslips")
        return betslips

database = DataBase()


new_user = User(email="user@gmail.com",username="username",password="pass123")

database.addUser(new_user)

user = database.getUser(1)

new_betslip = BetSlip(user_id=user.id,amount=1.30,winValue="20",won=False)

database.addBetSlip(new_betslip)

user = database.getUser(1)

print(user.__dict__['email'])

betslips = database.getUserBetslips(3)

for betslip in betslips:
    print(betslip.id)