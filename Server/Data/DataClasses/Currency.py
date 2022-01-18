from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.sqltypes import Float
from Data.Database import Base

class Currency(Base):
    __tablename__ = "Moeda"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45),primary_key=True, unique=True)
    value = Column("valor", Float)

    tax = 0.03

    def __init__(self,name,value) -> None:
        self.name = name
        self.value = value

    def convertToEUR(self,amount):
        return amount * self.value

    def convertFromEUR(self,amount):
        curTax = self.value + Currency.tax
        total = round(amount / curTax, 2)
        return total

    def updateValue(self, value):
        self.value = value