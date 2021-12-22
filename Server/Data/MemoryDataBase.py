from Data import DataBaseAccess
class MemoryDataBase(DataBaseAccess.DataBaseAccess):

    def __init__(self) -> None:
        self.currencies = ['Euros','Dollars','English_pounds','Cardans']
        self.users = {}
        self.events = {}
        self.bets = {}
        self.betslips = {}
        self.intervenors = {}
        self.sports = {}

    def getCurrencies(self):
        return self.currencies
