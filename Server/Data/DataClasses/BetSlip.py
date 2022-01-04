from Data.DataClasses import Bet
import enum

class BetSlipState(enum.Enum):
    Creating = 1 # Didn't bet yet
    InCourse = 2 # Waiting event results
    Finished = 3 # Finished bet

class BetSlip:
    
    idGenerator = 1

    def __init__(self) -> None:
        self.id = BetSlip.idGenerator
        BetSlip.idGenerator += 1
        self.user = -1
        self.amount = 0
        self.currency = ''
        self.winValue = 0
        self.bets = {'Finished':dict(),'Unfinished':dict()}
        self.state = BetSlipState.Creating
        self.inStake = 0
        self.won = 1

    def addBet(self,bet : Bet.Bet):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            allBets[bet.eventID] = bet

    def removeBet(self,eventID):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            if eventID in allBets:
                del allBets[eventID]
                return True
            else:
                return False

    def applyBetSlip(self):
        self.inStake = 1
        self.state = BetSlipState.InCourse
        for value in self.bets['Unfinished'].values():
            self.inStake *= value.odd
        self.inStake *= self.amount

    def updateBet(self,betID,result):
        if self.state is BetSlipState.InCourse:
            
            unfinishedBets = self.bets['Unfinished']
            bet = unfinishedBets.pop(betID)
            
            bet : Bet.Bet
            won = bet.checkResult(result)

            if won == False:
                won = 0
            
            self.bets['Finished'][bet.id] = bet
            
            if len(self.bets['Unfinished']) == 0:
                self.state = BetSlipState.Finished
                # Notify Users

