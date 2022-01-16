from Data.DataClasses.User_Currency import User_Currency
from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Boolean, Float
from Data.Database import Base

class Currency(Base):
    __tablename__ = "Moeda"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45),primary_key=True, unique=True)
    value = Column("valor", Float)

    #users = relationship('User_Currency', back_populates='currency')
    tax = 0.03

    def __init__(self,name,value) -> None:
        self.name = name
        self.value = value
        #self.users = []

    def convertToEUR(self,amount):
        return amount * self.value

    def convertFromEUR(self,amount):
        curTax = self.value + Currency.tax
        total = round(amount / curTax, 2)
        return total