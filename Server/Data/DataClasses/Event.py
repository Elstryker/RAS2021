import enum

from Data.DataClasses import Sport,Intervenor
from Data import Observable,Observer

class EventState(enum.Enum):
    Open = 1
    Suspended = 2
    Closed = 3

class Event(Observable.Observable):

    idGenerator = 1

    observers: list[Observer.Observer] = []

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
            self.notify()

    def getOdd(self,choice):
        return self.intervenors[choice][0]

    def toJSON(self):
        toReturn = dict()
        toReturn["Id"] = self.id

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

    def attach(self, observer: Observer.Observer) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer: Observer.Observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)