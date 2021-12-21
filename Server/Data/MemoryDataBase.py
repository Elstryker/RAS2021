from Data import DataBaseAccess

class MemoryDataBase(DataBaseAccess.DataBaseAccess):

    def __init__(self) -> None:
        self.availableCurrencies = ['Euros','Dollars','English pounds','Cardans']

    def getCurrencies(self):
        return self.availableCurrencies
