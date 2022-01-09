from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from Data.Database import Base

class User(Base):
    __tablename__ = 'Utilizador'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String(45), primary_key=True, unique=True)
    username = Column("nome", String(45), primary_key=True, unique=True)
    password = Column("password", String(45), nullable=False)
    messages = Column("mensagens", String(2000))
    #falta tabela para wallet
    wallet = relationship('User_Currency', back_populates='user')
    #wallet = Column("saldo",Float)
    #wallet = newCurrenciesDict(currencies)
    birthDate = Column("data_nascimento", Date)

    def __init__(self,username,password,email,birthDate,wallet) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.wallet = wallet
        self.birthDate = birthDate
        #self.currentBetSlip = betSlip
        #self.currentBetSlip.user = self.username

        self.messages = ""
        self.betSlips = {}

    def newCurrenciesDict(self,currencies : list):
        wallet = dict()
        for currency in currencies:
            wallet[currency] = 0
        return wallet

    def concludeBetSlip(self,newBetSlip):
        self.betSlips[self.currentBetSlip.id] = self.currentBetSlip
        self.currentBetSlip = newBetSlip

    
