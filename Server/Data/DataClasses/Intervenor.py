from Data.DataClasses import Intervenor_Event
from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from Data.Database import Base

class Intervenor(Base):
    __tablename__ = "Interveniente"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45), primary_key=True)
    events = relationship('Intervenor_Event', back_populates='intervenor')

    

    def __init__(self,name) -> None:
        self.name = name
        #self.events = []

    def addEvent(self,eventID):
        self.events.append(eventID)

    @classmethod
    def getParameters(cls) -> dict:
        params = dict()
        params["Name"] = 0

        return params