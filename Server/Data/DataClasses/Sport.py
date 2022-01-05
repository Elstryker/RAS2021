import enum
from Database import Base
from enum import unique
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base


class SportType(enum.Enum):
    Win = 1
    WinDraw = 2

class Sport(Base):
    __tablename__ = "Desporto"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45))
    type = Column("tipo", Enum(SportType))
    

    def __init__(self,type : SportType,name) -> None:
        self.name = name
        self.type = type
        self.events = []

    def addEvent(self,eventID):
        self.events.append(eventID)

    def toJSON(self):
        toReturn = dict()

        toReturn["Name"] = self.name
        toReturn["Type"] = self.type.name

        return toReturn

    @classmethod
    def getParameters(cls) -> dict:
        params = dict()
        params["Name"] = 0
        types = []
        for type in SportType:
            types.append(type.name)

        params["Type"] = types
        return params