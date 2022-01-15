from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Boolean, Float
import enum

class BetSlipState(enum.Enum):
    Creating = 1 # Didn't bet yet
    InCourse = 2 # Waiting event results
    Finished = 3 # Finished bet

from Data.DataClasses.Event import Event, EventState
from Data.Database import Base
from Data.DataClasses import Bet





class BetSlip(Base):
    __tablename__ = "Boletim"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("utilizador_id", Integer,ForeignKey('Utilizador.id'))
    user = relationship('User', backref=backref('betslips', uselist=True))
    amount = Column("montante",Float)
    win_value = Column("valor_vitoria",Float)
    multiplied_odd = Column("odd_total",Float)
    won = Column("acertou",Boolean)
    state = Column("estado", Enum(BetSlipState))
    currency_id = Column("moeda_id", Integer,ForeignKey('Moeda.id'))
    currency = relationship('Currency')


    def __init__(self,user,amount=0,win_value=0,won=True,currency=None,multiplied_odd=1):
        self.user = user
        self.amount = amount
        self.currency = currency
        self.win_value = win_value
        self.multiplied_odd = multiplied_odd
        self.won = won
        self.bets = []
        self.state = BetSlipState.Creating

    def addBet(self,bet : Bet.Bet):
        if self.state is BetSlipState.Creating:
            self.bets.append(bet)
            self.multiplied_odd *= bet.odd

    def removeBet(self,eventID):
        if self.state is BetSlipState.Creating:
            for bet in self.bets:
                if bet.event_id == eventID:
                    self.bets.remove(bet)
                    return True
        return False

    def isCreating(self):
        return self.state == BetSlipState.Creating

    def applyBetSlip(self, amount, currency):
        self.state = BetSlipState.InCourse
        self.amount = amount
        self.currency = currency
        self.win_value = self.amount * self.multiplied_odd

    def updateBet(self,eventID,result):
        if self.state is BetSlipState.InCourse:
            unfinishedBets = []
            for bet in self.bets:
                if(bet.event.state == EventState.Open):
                    unfinishedBets.append(bet)
            
            for bet in self.bets:
                if bet.event.id == eventID:
                    update_bet = bet

            update_bet : Bet.Bet
            won = update_bet.checkResult(result)

            if won == False:
                self.won = False
            
            #self.bets['Finished'][bet.id] = bet
            
            if len(unfinishedBets) == 0:
                self.state = BetSlipState.Finished
                # Notify Users

    def toJSON(self):
        jsonToSend = dict()

        bets = self.bets

        jsonToSend["Id"] = self.id

        jsonToSend["Bets"] = [x.toJSON() for x in bets.values()]
        if self.amount != 0:
            jsonToSend["Amount"] = self.amount
        
        if self.currency != None:
            jsonToSend["Currency"] = self.currency.name

        jsonToSend["MultipliedOdd"] = self.multiplied_odd

        jsonToSend["State"] = self.state.name

        if self.inStake != 0:
            jsonToSend["InStake"] = self.win_value

        if self.state is BetSlipState.Finished:
            jsonToSend["Won"] = self.won

        return jsonToSend

    def update(self, info : Event) -> None:
        print("BetSlip: Update requested!")
        self.updateBet(info.id,info.result)