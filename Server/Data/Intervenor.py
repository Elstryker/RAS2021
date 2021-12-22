class Intervenor:
    
    idGenerator = 1

    def __init__(self,name) -> None:
        self.id = self.idGenerator
        self.idGenerator += 1
        self.name = name
        self.events = []

    def addEvent(self,eventID):
        self.events.append(eventID)