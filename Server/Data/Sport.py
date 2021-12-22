import enum
class SportType(enum.Enum):
    Win = 1
    WinDraw = 2

class Sport:
    
    idGenerator = 1

    def __init__(self,type : SportType,name) -> None:
        self.id = self.idGenerator
        self.idGenerator += 1
        self.name = name
        self.type = type
        self.events = []

    def addEvent(self,eventID):
        self.events.append(eventID)