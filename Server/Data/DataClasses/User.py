from DataClasses.BetSlip import BetSlip
from DataClasses.User_Currency import User_Currency
from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Boolean, Float
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.util.langhelpers import memoized_instancemethod
from sqlalchemy_utils import database_exists, create_database
from Database import Base

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

    def depositMoney(self,amount,currency):
        self.wallet[currency] += amount

    def withdrawMoney(self,amount,currency):
        if self.wallet[currency] >= amount:
            self.wallet[currency] -= amount

    def concludeBetSlip(self,newBetSlip : BetSlip):
        self.betSlips[self.currentBetSlip.id] = self.currentBetSlip
        self.currentBetSlip = newBetSlip

    
