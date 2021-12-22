import Bet, enum

class BetSlipState(enum.Enum):
    Creating = 1 # Didn't bet yet
    InCourse = 2 # Waiting event results
    Finished = 3 # Finished bet

class BetSlip:
    
    idGenerator = 1

    def __init__(self,userID) -> None:
        self.id = self.idGenerator
        self.idGenerator += 1
        self.amount = 0
        self.currency = ''
        self.winValue = 0
        self.bets = {'Finished':dict(),'Unfinished':dict()}
        self.user = userID
        self.state = BetSlipState.Creating
        self.inStake = 0
        self.won = 1

    def addBet(self,bet : Bet.Bet):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            allBets[bet.id] = bet

    def removeBet(self,betID):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            del allBets[betID]

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

