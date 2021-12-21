import RASBetFacade
from Data import DataBaseAccess

class RASBetLN(RASBetFacade.RASBetFacade):

    db = DataBaseAccess

    def __init__(self,db : DataBaseAccess) -> None:
        self.db = db

    def depositMoney(self,userID,currency,amount):
        print(f"User {userID} deposited: {amount} {currency}")

    def withdrawMoney(self,userID,currency,amount):
        print(f"User {userID} withdrawed: {amount} {currency}")

    def addBetToBetSlip(self,userID,eventID,result):
        print(f"User {userID} bett on event {eventID}, on {result}")

    def removeBetFromBetSlip(self,userID,eventID):
        print(f"User {userID} removed bett on event {eventID}")

    def showBetSlip(self,userID):
        print(f"User {userID} bet slip")

    def cancelBetSlip(self,userID):
        print(f"User {userID} cancelled his bet slip")

    def getCurrencies(self):
        return self.db.getCurrencies()
        

    


    
