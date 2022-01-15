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
    birthDate = Column("data_nascimento", Date)

    def __init__(self,username,password,email,birthDate) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.wallet = []
        self.birthDate = birthDate

        self.messages = ""
        self.betSlips = {}
        self.notifications = []

    #não recomendado
    #currencies já são adicionadas automaticamente
    def newCurrenciesDict(self,currencies : list):
        wallet = dict()
        for currency in currencies:
            wallet[currency] = 0
        return wallet

    def getCurrentBetSlip(self):
        for betslip in self.betSlips:
            if betslip.isCreating():
                return betslip

    def getHistory(self) -> list :
        history = []
        for betslip in self.betSlips:
            if not betslip.isCreating():
                history.append(betslip)
        return history
        
    def concludeBetSlip(self,newBetSlip):
        self.betSlips.append(newBetSlip)

    def retrieveNotifications(self):
        notifs = self.messages.split("|")
        self.messages = ""
        return notifs

    def update(self, info: dict) -> None:
        currency = info["Currency"]
        total = info["InStake"]
        won = info["Won"]
        print(f"InStake: {total}")
        if won:
            self.wallet[currency] += total
            self.notifications.append(f"Won {total} {currency} from a bet slip")
        else:
            self.notifications.append("One of your bet slips did not win")
        print("User: Update requested!")

    

    
