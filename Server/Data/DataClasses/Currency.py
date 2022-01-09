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

class Currency(Base):
    __tablename__ = "Moeda"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45),primary_key=True, unique=True)
    value = Column("valor", Float)
    users = relationship('User_Currency', back_populates='currency')

    

    def __init__(self,name,value) -> None:
        self.name = name
        self.value = value
        #self.users = []

    @classmethod
    def getParameters(cls) -> dict:
        params = dict()
        params["Name"] = 0

        return params