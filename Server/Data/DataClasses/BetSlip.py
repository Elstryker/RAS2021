from Data.DataClasses import Bet,Event
import enum
from Data import Observer,Observable

class BetSlipState(enum.Enum):
    Creating = 1 # Didn't bet yet
    InCourse = 2 # Waiting event results
    Finished = 3 # Finished bet

class BetSlip(Observable.Observable,Observer.Observer):
    
    idGenerator = 1

    observers: list[Observer.Observer]

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
        self.observers = []

    def addBet(self,bet : Bet.Bet):
        if self.state is BetSlipState.Creating:
            allBets = self.bets['Unfinished']
            if bet.event.id in allBets:
                self.removeBet(bet.event.id)
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
        self.inStake = round(self.amount * self.multipliedOdd,2)


    def updateBet(self,eventID,result):
        if self.state is BetSlipState.InCourse:
            
            unfinishedBets = self.bets['Unfinished']
            bet = unfinishedBets.pop(eventID)
            
            bet : Bet.Bet
            won = bet.checkResult(result)

            if won == False:
                self.winning = False
            
            self.bets['Finished'][bet.id] = bet
            
            if len(self.bets['Unfinished']) == 0:
                self.state = BetSlipState.Finished
                self.notify()

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

        if self.state is BetSlipState.Finished:
            jsonToSend["Won"] = self.winning

        return jsonToSend

    def attach(self, observer: Observer.Observer) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer: Observer.Observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        info = {"InStake":self.inStake,"Won":self.winning,"Currency":self.currency}
        for observer in self.observers:
            observer.update(info)

    def update(self, info : Event.Event) -> None:
        self.updateBet(info.id,info.result)