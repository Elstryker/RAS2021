
class RASBetFacade:
    
    def depositMoney(self,userID,currency,amount):
        pass

    def withdrawMoney(self,userID,currency,amount):
        pass

    def addBetToBetSlip(self,userID,args):
        pass

    def removeBetFromBetSlip(self,userID,eventID):
        pass

    def getBetSlip(self,userID):
        pass

    def getBetSlip(self,userID):
        pass
    
    def concludeBetSlip(self,userID,amount,currency):
        pass

    def getBetHistory(self,userID):
        pass

    def exchangeMoney(self,userID,fromCur,toCur,amount):
        pass

    def login(self,userID,password,prevBetSlip): 
        pass
    
    def logout(self,userID):
        pass

    def register(self,userID,password,birthdate,email):
        pass

    def getDefaultInfo(self,userID):
        pass

    # ---------------------------------------- Bookie Methods ---------------------------------------- #
        
    def addEvent(self,args):
        pass

    def addSport(self,args):
        pass

    def addIntervenor(self,args):
        pass

    def startEvent(self,args):
        pass

    def concludeEvent(self,args):
        pass

    def addCurrency(self,currency,toEUR):
        pass
    
    def removeCurrency(self,currency):
        pass

    def updateCurrencyExchange(self,currency,exchangeValue):
        pass