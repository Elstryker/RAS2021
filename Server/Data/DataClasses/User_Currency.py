from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import  Float
from Data.Database import Base

class User_Currency(Base):
    __tablename__ = "Utilizador_Moeda"
    user_id = Column("utilizador_id",Integer,ForeignKey('Utilizador.id'),primary_key=True)
    currency_id = Column("moeda_id",Integer,ForeignKey('Moeda.id'), primary_key=True)
    user = relationship("User", back_populates="wallet")
    currency = relationship("Currency")
    amount = Column("quantidade", Float)


    def __init__(self,user,currency,amount) -> None:
        self.user = user
        self.currency = currency
        self.amount = amount