class RASBetFacade:
    
    def depositMoney(self,userID,currency,amount):
        pass

    def withdrawMoney(self,userID,currency,amount):
        pass

    def addBetToBetSlip(self,userID,eventID,result):
        pass

    def removeBetFromBetSlip(self,userID,eventID):
        pass

    def showBetSlip(self,userID):
        pass

    def cancelBetSlip(self,userID):
        pass
    
    def concludeBetSlip(self,userID,amount,currency):
        pass
    
    def getEvents(self,offset,numOfEvents):
        pass

    def login(self,username,password) -> int:
        pass
    
    def register(self,username,password,birthdate):
        pass

    def getCurrencies(self):
        pass