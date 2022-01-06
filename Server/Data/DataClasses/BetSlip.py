from Data.DataClasses import Bet
import enum

class BetSlipState(enum.Enum):
    Creating = 1 # Didn't bet yet
    InCourse = 2 # Waiting event results
    Finished = 3 # Finished bet

class BetSlip:
    
    idGenerator = 1

    user : int
    amount : float
    currency : str
    bets : dict[str,dict[int,Bet.Bet]]
    state : BetSlipState
    multipliedOdd : float
    inStake : float

    def __init__(self) -> None:
        self.id = BetSlip.idGenerator
        BetSlip.idGenerator += 1
        self.user = -1
        self.amount = 0
        self.currency = ''
        self.bets = {'Finished':dict(),'Unfinished':dict()}
        self.state = BetSlipState.Creating
        self.multipliedOdd = 1
        self.inStake = 0
        self.winning = True

    def addBet(self,bet : Bet.Bet):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            allBets[bet.event.id] = bet
            self.multipliedOdd *= bet.odd

    def removeBet(self,eventID):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            if eventID in allBets:
                self.multipliedOdd /= allBets[eventID].odd
                del allBets[eventID]
                return True
            else:
                return False

    def applyBetSlip(self,amount,currency):
        self.state = BetSlipState.InCourse
        self.amount = amount
        self.currency = currency
        self.inStake = self.amount * self.multipliedOdd


    def updateBet(self,betID,result):
        if self.state is BetSlipState.InCourse:
            
            unfinishedBets = self.bets['Unfinished']
            bet = unfinishedBets.pop(betID)
            
            bet : Bet.Bet
            won = bet.checkResult(result)

            if won == False:
                self.winning = False
            
            self.bets['Finished'][bet.id] = bet
            
            if len(self.bets['Unfinished']) == 0:
                self.state = BetSlipState.Finished
                # Notify Users

    def cancel(self):
        self.bets.clear()
        self.bets = {'Finished':dict(),'Unfinished':dict()}
        self.multipliedOdd = 1

    def toJSON(self):
        jsonToSend = dict()

        bets = self.bets["Unfinished"]
        bets.update(self.bets["Finished"])

        jsonToSend["Id"] = self.id

        jsonToSend["Bets"] = [x.toJSON() for x in bets.values()]
        if self.amount != 0:
            jsonToSend["Amount"] = self.amount
        
        if self.currency != '':
            jsonToSend["Currency"] = self.currency

        jsonToSend["MultipliedOdd"] = self.multipliedOdd

        jsonToSend["State"] = self.state.name

        if self.inStake != 0:
            jsonToSend["InStake"] = self.inStake

        return jsonToSend