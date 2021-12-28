from Data.DataClasses import BetSlip

class DataBaseAccess:
    
    def getCurrencies(self) -> list:
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

    def getBetSlip(self,username) -> BetSlip.BetSlip:
        pass

    def depositMoney(self,username,currency,amount) -> None:
        pass

    def withdrawMoney(self,username,currency,amount) -> bool:
        pass

    def getUserTotalBalance(self,username) -> dict:
        pass

    def getAvailableEvents(self,page,eventsPerPage) -> list:
        pass

    def getParameters(self,obj) -> dict:
        pass

    def createSport(self,name,type) -> bool:
        pass

    def createIntervenor(self,name) -> bool:
        pass

    def createEvent(self,name,sport,intervenors,odds) -> bool:
        pass
