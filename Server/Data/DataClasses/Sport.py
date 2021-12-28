import enum
class SportType(enum.Enum):
    Win = 1
    WinDraw = 2

class Sport:
    
    idGenerator = 1

    def __init__(self,type : SportType,name) -> None:
        self.id = Sport.idGenerator
        Sport.idGenerator += 1
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