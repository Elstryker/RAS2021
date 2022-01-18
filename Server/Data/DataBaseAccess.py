class DataBaseAccess:
    
    def getCurrencies(self) -> dict:
        pass

    def existsUser(self,username) -> bool:
        pass

    def createUser(self,username,password,birthdate) -> None:
        pass

    def authenticateUser(self,username,password) -> bool:
        pass

    def getBetSlip(self,username):
        pass

    def depositMoney(self,username,currency,amount) -> None:
        pass

    def withdrawMoney(self,username,currency,amount) -> bool:
        pass

    def getUserTotalBalance(self,username) -> dict:
        pass

    def getAvailableEvents(self) -> list:
        pass

    def getParameters(self,obj) -> dict:
        pass

    def createSport(self,name,type,collectiveness):
        pass

    def createIntervenor(self,name) -> bool:
        pass

    def createEvent(self,eventName, sport, intervenors, odds):
        pass

    def startEvent(self,eventID) -> bool:
        pass

    def concludeEvent(self,eventID,result) -> None:
        pass

    def getSuspendedEvents(self) -> list:
        pass
    
    def getEvent(self,eventID):
        pass

    def addBetToBetSlip(self,username,eventID,result) -> bool:
        pass

    def removeBetFromBetSlip(self,username,eventID) -> bool:
        pass

    def cancelBetSlip(self,username) -> None:
        pass

    def checkBetSlipConclusion(self,username) -> bool:
        pass

    def concludeBetSlip(self,username,amount,currency) -> bool:
        pass

    def getUserHistory(self,username):
        pass

    def addCurrency(self,currency,toEUR) -> bool:
        pass

    def updateCurrencyValue(self, currencyName, value):
        pass

    def removeCurrency(self, currencyName) -> bool:
        pass

    def retrieveNotifications(self,username) -> list:
        pass