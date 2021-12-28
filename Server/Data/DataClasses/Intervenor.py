class Intervenor:
    
    idGenerator = 1

    def __init__(self,name) -> None:
        self.id = Intervenor.idGenerator
        Intervenor.idGenerator += 1
        self.name = name
        self.events = []

    def addEvent(self,eventID):
        self.events.append(eventID)

    @classmethod
    def getParameters(cls) -> dict:
        params = dict()
        params["Name"] = 0

        return params