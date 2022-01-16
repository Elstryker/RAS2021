from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Boolean, Float
from Data.Database import Base

class Intervenor_Event(Base):
    __tablename__ = "Interveniente_Evento"
    event_id = Column("evento_id",Integer,ForeignKey('Evento.id'),primary_key=True)
    invervenor_id = Column("interveniente_id",Integer,ForeignKey('Interveniente.id'),primary_key=True)
    event = relationship("Event", back_populates="intervenors")
    intervenor = relationship("Intervenor", back_populates="events")
    odd = Column("odd", Float)


    def __init__(self,intervenor,event,odd) -> None:
        self.intervenor = intervenor
        self.event = event
        self.odd = odd
        #self.events = []