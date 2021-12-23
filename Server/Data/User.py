from Data import BetSlip


class User:

    def __init__(self,username,password,currencies : list,birthDate,betSlip : BetSlip.BetSlip) -> None:
        self.username = username
        self.password = password
        self.wallet = self.newCurrenciesDict(currencies)
        self.birtDate = birthDate
        self.currentBetSlip = betSlip
        self.betSlips = {}

    def newCurrenciesDict(self,currencies : list):
        wallet = {}
        for currency in currencies:
            wallet[currency] = 0

    def depositMoney(self,amount,currency):
        self.wallet[currency] += amount

    def withdrawMoney(self,amount,currency):
        if self.wallet[currency] >= amount:
            self.wallet[currency] -= amount

    def concludeBetSlip(self,newBetSlip : BetSlip.BetSlip):
        self.betSlips[self.currentBetSlip.id] = self.currentBetSlip
        self.currentBetSlip = newBetSlip

    
