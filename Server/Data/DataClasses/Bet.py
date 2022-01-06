from Data.DataClasses import Event


class Bet:
    
    idGenerator = 1

    result : int
    event : Event.Event
    betslipID : int
    odd : float

    def __init__(self,result,odd,event,betslipID) -> None:
        self.id = Bet.idGenerator
        Bet.idGenerator += 1
        self.result = result
        self.event = event
        self.betslipID = betslipID
        self.odd = odd

    def checkResult(self,result):
        if self.result == result:
            won = True
        else:
            won = False
        return won
    
    def toJSON(self):
        eventJSON = self.event.toJSON()

        jsonToSend = dict()

        jsonToSend["EventID"] = eventJSON["Id"]
        jsonToSend["EventName"] = eventJSON["Name"]
        jsonToSend["Choice"] = eventJSON["Intervenors"][self.result][1] # Get the choise with result var and then getting the intervenor name from tuple (odd,intervenor)
        jsonToSend["Odd"] = self.odd

        return jsonToSend

