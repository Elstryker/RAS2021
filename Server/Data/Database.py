""" from Data.DataClasses import BetSlip,User,Event,Bet,Intervenor,Sport
from Data import DataBaseAccess
from Data.DataClasses.Sport import SportType """
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.sql.sqltypes import Boolean, Float
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.util.langhelpers import memoized_instancemethod
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()

class User(Base):
    __tablename__ = 'Utilizador'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String(45))
    username = Column("nome", String(45))
    password = Column("password", String(45))
    wallet = Column("saldo",Float)
    messages = Column("mensagens", String(1000))
    #wallet = newCurrenciesDict(currencies)
    birthDate = Column("data_nascimento", Date)

class BetSlip(Base):
    __tablename__ = "Boletim"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("utilizador_id", Integer,ForeignKey('Utilizador.id'))
    user = relationship(User)
    amount = Column("montante",Float)
    winValue = Column("valor_vitoria",Float)
    won = Column("acertou",Boolean)


""" class DataBase(DataBaseAccess.DataBaseAccess): """
class DataBase():

    def __init__(self) -> None:
        self.engine = create_engine("mysql://admin:password@localhost/rasbetDB", connect_args= dict(host='localhost', port=3306))
        self.session = Session(self.engine)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        Base.metadata.create_all(self.engine)

    def add(self):
        
        new_user = User(email="user@gmail.com",username="username",password="pass123")
        self.session.add(new_user)

        new_betslip = BetSlip(user=new_user,amount=1.30,winValue="20",won=False)
        self.session.add(new_betslip)

        self.session.commit()        

    def getUser(self, user_id: Integer) -> User:
        user = self.session.query(User).filter(User.id == user_id).one()
        print(user.email)
        return user
        
    def getUserBetslips(self, user: User):
        betslips = self.session.query(BetSlip).filter(BetSlip.user == user).one()
        print(betslips)
        return betslips

database = DataBase()

database.add()

user = database.getUser(1)

betslips = database.getUserBetslips(user)

print(betslips.winValue)