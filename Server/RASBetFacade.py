from Data.DataClasses import BetSlip


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

    def getBetSlip(self,userID) -> BetSlip.BetSlip:
        pass
    
    def concludeBetSlip(self,userID,amount,currency):
        pass
    
    def getEvents(self,offset,numOfEvents):
        pass

    def getBetHistory(self,username):
        pass

    def login(self,prevID,username,password):
        pass
    
    def logout(self,username):
        pass

    def register(self,username,password,birthdate):
        pass

    def getCurrencies(self):
        pass