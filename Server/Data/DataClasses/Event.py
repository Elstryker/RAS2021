import enum
from Data.DataClasses import Sport, Intervenor_Event
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from Data.Database import Base


class EventState(enum.Enum):
    Open = 1
    Suspended = 2
    Closed = 3

class Event(Base):
    __tablename__ = "Evento"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45),primary_key=True)
    state = Column("estado", Enum(EventState))
    sport_id = Column("desporto_id", Integer,ForeignKey('Desporto.id'))
    sport = relationship(Sport.Sport, backref=backref("events", uselist=True))
    intervenors = relationship('Intervenor_Event', back_populates='event')
    result = Column("resultado", Integer)

    def __init__(self,name,sport : Sport.Sport,intervenors : list[Intervenor_Event.Intervenor_Event]) -> None:

        self.name = name
        self.state = EventState.Open
        self.sport = sport
        self.intervenors = intervenors
        self.result = -1 # -1 -> Not Known

    def initiateEvent(self):
        if self.state is EventState.Open:
            self.state = EventState.Suspended

    def terminateEvent(self,result):
        if self.state is EventState.Suspended:
            self.state = EventState.Closed
            self.result = result
            # Notify Bets

    def getOdd(self,choice):
        return self.intervenors[choice][0]

    def toJSON(self):
        toReturn = dict()
        toReturn["Id"] = self.id

        toReturn["Name"] = self.name

        toReturn["Sport"] = self.sport.toJSON()

        intervenors = []
        for intervenor_event in self.intervenors:
            if intervenor_event != None:
                intervenors.append([intervenor_event.odd,intervenor_event.intervenor.name])
        toReturn["Intervenors"] = intervenors

        return toReturn