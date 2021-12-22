class Bet:
    
    idGenerator = 1

    def __init__(self,result,odd,event,betslip) -> None:
        self.id = self.idGenerator
        self.idGenerator += 1
        self.result = result
        self.event = event
        self.betslip = betslip
        self.odd = odd

    def checkResult(self,result):
        if self.result == result:
            won = True
        else:
            won = False
        return won
    