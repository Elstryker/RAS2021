import enum
from Data.Database import Base
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.sql.sqltypes import Boolean

class SportType(enum.Enum):
    Win = 1
    WinDraw = 2

class Sport(Base):
    __tablename__ = "Desporto"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String(45), primary_key=True, unique=True)
    type = Column("tipo", Enum(SportType))
    isCollective = Column("coletivo",Boolean)

    def __init__(self,type : SportType,name, isCollective) -> None:
        self.name = name
        self.type = type
        self.events = []
        self.isCollective = isCollective

    def addEvent(self,eventID):
        self.events.append(eventID)

    def toJSON(self):
        toReturn = dict()

        toReturn["Name"] = self.name
        toReturn["Type"] = self.type.name
        toReturn["Collectiveness"] = self.isCollective

        return toReturn

    @classmethod
    def getParameters(cls) -> dict:
        params = dict()
        params["Name"] = 0
        types = []
        for type in SportType:
            types.append(type.name)

        params["Type"] = types
        params["Collectiveness"] = ["True","False"]
        return params