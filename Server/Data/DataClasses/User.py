from Data.DataClasses import BetSlip
from Data import Observer,Observable

class User(Observer.Observer):

    def __init__(self,username,password,currencies : list,birthDate,betSlip : BetSlip.BetSlip) -> None:
        self.username = username
        self.password = password
        self.wallet = self.newCurrenciesDict(currencies)
        self.birtDate = birthDate
        self.currentBetSlip = betSlip
        self.currentBetSlip.user = self.username
        self.betSlips = {}
        self.notifications = []

    def newCurrenciesDict(self,currencies : list):
        wallet = dict()
        for currency in currencies:
            wallet[currency] = 0
        return wallet

    def depositMoney(self,amount,currency):
        self.wallet[currency] += amount

    def withdrawMoney(self,amount,currency):
        if self.wallet[currency] >= amount:
            self.wallet[currency] -= amount

    def retrieveNotifications(self):
        notifs = self.notifications.copy()
        self.notifications.clear()
        return notifs

    def concludeBetSlip(self,newBetSlip : BetSlip.BetSlip):
        self.betSlips[self.currentBetSlip.id] = self.currentBetSlip
        self.currentBetSlip = newBetSlip

    def update(self, info: dict) -> None:
        currency = info["Currency"]
        total = info["InStake"]
        won = info["Won"]
        print(f"InStake: {total}")
        if won:
            self.wallet[currency] += total
            self.notifications.append((1,(total,currency))) #f"Won {total} {currency} from a bet slip"
        else:
            self.notifications.append((0,None)) #"One of your bet slips did not win"
        print("User: Update requested!")

    

    
