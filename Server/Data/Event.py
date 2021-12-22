import enum

from Server.Data.Sport import Sport
class EventState(enum.Enum):
    Open = 1
    Suspended = 2
    Closed = 3

class Event:

    idGenerator = 1

    def __init__(self,sport : Sport,intervenors : list) -> None:
        self.id = self.idGenerator
        self.idGenerator += 1
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