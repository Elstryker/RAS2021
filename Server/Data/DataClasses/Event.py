import enum

from Data.DataClasses import Sport,Intervenor

class EventState(enum.Enum):
    Open = 1
    Suspended = 2
    Closed = 3

class Event:

    idGenerator = 1

    def __init__(self,name,sport : Sport.Sport,intervenors : list[tuple[float,Intervenor.Intervenor]]) -> None:
        self.id = Event.idGenerator
        Event.idGenerator += 1
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

    def toJSON(self):
        toReturn = dict()
        toReturn["Name"] = self.name

        toReturn["Sport"] = self.sport.toJSON()

        intervenors = []
        for odd, intervenor in self.intervenors:
            if intervenor != None:
                intervenors.append([odd,intervenor.name])
            else:
                intervenors.append([odd,"Draw"])
        toReturn["Intervenors"] = intervenors

        return toReturn