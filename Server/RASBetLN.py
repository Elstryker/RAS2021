import RASBetFacade
from Data import DataBaseAccess

class RASBetLN(RASBetFacade.RASBetFacade):

    db = DataBaseAccess

    def __init__(self,db : DataBaseAccess) -> None:
        self.db = db

    def depositMoney(self,userID,amount):
        print(f"User {userID} deposited: {amount}€")
