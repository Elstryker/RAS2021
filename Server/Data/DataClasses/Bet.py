from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref
from Database import Base

class Bet(Base):
    __tablename__ = "Aposta"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    event_id = Column("evento_id",Integer,ForeignKey('Evento.id'),primary_key=True)
    event = relationship("Event", backref=backref('bets', uselist=True))
    betslip_id = Column("boletim_id",Integer,ForeignKey('Boletim.id'),primary_key=True)
    betslip = relationship("BetSlip", backref=backref('bets', uselist=True))
    

    def __init__(self,betslip, event) -> None:
        self.event = event
        self.betslip = betslip

    def checkResult(self,result):
        if self.result == result:
            won = True
        else:
            won = False
        return won
    