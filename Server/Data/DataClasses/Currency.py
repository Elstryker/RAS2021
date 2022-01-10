class Currency:

    tax = 0.03

    def __init__(self,name,toEUR) -> None:
        self.name = name
        self.toEUR = toEUR

    def convertToEUR(self,amount):
        return amount * self.toEUR

    def convertFromEUR(self,amount):
        curTax = self.toEUR + Currency.tax
        total = round(amount / curTax, 2)
        return total