from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from Data.Database import Base

class Intervenor(Base):
    __tablename__ = "Interveniente"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45), primary_key=True)
    events = relationship('Intervenor_Event', back_populates='intervenor', uselist=True)

    def __init__(self,name) -> None:
        self.name = name

    def addEvent(self,eventID):
        self.events.append(eventID)

    @classmethod
    def getParameters(cls) -> dict:
        params = dict()
        params["Name"] = 0

        return params