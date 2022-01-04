class Bet:
    
    idGenerator = 1

    def __init__(self,result,odd,eventID,betslipID) -> None:
        self.id = Bet.idGenerator
        Bet.idGenerator += 1
        self.result = result
        self.eventID = eventID
        self.betslipID = betslipID
        self.odd = odd

    def checkResult(self,result):
        if self.result == result:
            won = True
        else:
            won = False
        return won
    