

from enum import unique
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Boolean, Float
from Data.Database import Base
from Data.DataClasses.Bet import Bet
import enum


class BetSlipState(enum.Enum):
    Creating = 1 # Didn't bet yet
    InCourse = 2 # Waiting event results
    Finished = 3 # Finished bet

class BetSlip(Base):
    __tablename__ = "Boletim"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("utilizador_id", Integer,ForeignKey('Utilizador.id'))
    user = relationship('User', backref=backref('betslips', uselist=True))
    amount = Column("montante",Float)
    win_value = Column("valor_vitoria",Float)
    won = Column("acertou",Boolean)
    state = Column("estado", Enum(BetSlipState))


    def __init__(self,user,amount,win_value,won):
        self.user = user
        self.amount = amount
        self.currency = ''
        self.win_value = win_value
        self.bets = []
        self.state = BetSlipState.Creating
        self.inStake = 0
        self.won = won

    def addBet(self,bet : Bet):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            allBets[bet.eventID] = bet

    def removeBet(self,eventID):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            if eventID in allBets:
                del allBets[eventID]
                return True
            else:
                return False

    def applyBetSlip(self):
        self.state = BetSlipState.InCourse

    def updateBet(self,betID,result):
        if self.state is BetSlipState.InCourse:
            
            unfinishedBets = self.bets['Unfinished']
            bet = unfinishedBets.pop(betID)
            
            bet : Bet.Bet
            won = bet.checkResult(result)

            if won == False:
                won = 0
            
            self.bets['Finished'][bet.id] = bet
            
            if len(self.bets['Unfinished']) == 0:
                self.state = BetSlipState.Finished
                # Notify Users

