from enum import unique
from sqlalchemy import Column, String, Integer, Float, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref
from Data.Database import Base

class Bet(Base):
    __tablename__ = "Aposta"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    event_id = Column("evento_id",Integer,ForeignKey('Evento.id'),primary_key=True)
    event = relationship("Event", backref=backref('bets', uselist=True))
    intervenor_id = Column("interveniente_id",Integer,ForeignKey('Interveniente.id'),primary_key=True)
    intervenor = relationship("Intervenor", backref=backref('bets', uselist=True))
    betslip_id = Column("boletim_id",Integer,ForeignKey('Boletim.id'),primary_key=True)
    betslip = relationship("BetSlip", backref=backref('bets', uselist=True))
    #result = Column("resultado",Integer)
    odd = Column("odd", Float)
    

    def __init__(self,betslip, event, intervenor, odd) -> None:
        self.event = event
        self.betslip = betslip
        self.intervenor = intervenor
        #self.result = result
        self.odd = odd

    def checkResult(self,result):
        for i, int_event in enumerate(self.event.intervenors):
            if int_event.intervenor == self.intervenor:
                return (i == result)
    
    def toJSON(self):
        eventJSON = self.event.toJSON()

        jsonToSend = dict()

        jsonToSend["EventID"] = eventJSON["Id"]
        jsonToSend["EventName"] = eventJSON["Name"]
        jsonToSend["Choice"] = self.intervenor.name # Get the choice with result var and then getting the intervenor name from tuple (odd,intervenor)
        jsonToSend["Odd"] = self.odd

        return jsonToSend
