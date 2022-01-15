class DataBaseAccess:
    
    def getCurrencies(self) -> dict:
        pass

    def existsUser(self,username) -> bool:
        pass

    def createUser(self,username,password,birthdate) -> None:
        pass

    def authenticateUser(self,username,password) -> bool:
        pass

    # Replaces non logged in user bet slip with the logged in user one
    def updateBetSlip(self,prevID,username) -> None:
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

    def createSport(self,name,type) -> bool:
        pass

    def createIntervenor(self,name) -> bool:
        pass

    def createEvent(self,name,sport,intervenors,odds) -> bool:
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

    def concludeBetSlip(self,username,amount,currency) -> None:
        pass

    def getUserHistory(self,username):
        pass

    def addCurrency(self,currency,toEUR) -> bool:
        pass

    def removeCurrency(self,currency) -> None:
        pass

    def retrieveNotifications(self,username) -> list:
        pass