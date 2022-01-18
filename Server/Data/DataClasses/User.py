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
    wallet = relationship('User_Currency', back_populates='user')
    birthDate = Column("data_nascimento", Date)

    def __init__(self,username,password,email, birthDate) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.wallet = []
        self.birthDate = birthDate

        self.messages = ""
        self.betSlips = {}
        self.notifications = []

    def getCurrentBetSlip(self):
        for betslip in self.betSlips:
            if betslip.isCreating():
                return betslip

    def getHistory(self) -> list :
        history = []
        for betslip in self.betslips:
            if not betslip.isCreating():
                history.append(betslip)
        return history
        
    def concludeBetSlip(self,newBetSlip):
        self.betSlips.append(newBetSlip)

    def retrieveNotifications(self):
        if len(self.messages) > 0:
            notifs = self.messages.split("|")
            self.messages = ""
            return notifs
        else:
            return []

    def update(self, info: dict) -> None:
        currency = info["Currency"]
        total = info["InStake"]
        won = info["Won"]
        if won:
            for u_currency in self.wallet:
                if u_currency.currency.name == currency:
                    u_currency.amount += total
            if len(self.messages) > 0:
                self.messages += f"|Won {total} {currency} from a bet slip"
            else:
                self.messages += f"Won {total} {currency} from a bet slip"
        else:
            if len(self.messages) > 0:
                self.messages += ("|One of your bet slips did not win")
            else:
                self.messages += ("One of your bet slips did not win")

        print("User: Update requested!")

    

    
