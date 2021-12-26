import RASBetFacade
from Data import DataBaseAccess
import datetime, json

class RASBetLN(RASBetFacade.RASBetFacade):
    # TODO: Have memory structure to have client session data for correct continuous data fetching

    db : DataBaseAccess.DataBaseAccess
    sessionsInfo : dict # userID -> ["Page"]

    def __init__(self,db : DataBaseAccess.DataBaseAccess) -> None:
        self.db = db
        self.sessionsInfo = dict()

    def createDictWithDefaultInfo(self,userID):
        if userID not in self.sessionsInfo:
            self.sessionsInfo[userID] = {"Page":0,"EventsPerPage":5}

        # sessionInfo = self.sessionsInfo[userID] -> Next
        toSend = dict()
        toSend["Wallet"] = self.db.getUserTotalBalance(userID)
        toSend["Events"] = [] # self.db.getAvailableEvents(sessionInfo["Page"],sessionInfo["EventsPerPage"]) -> Next
        toSend["Currencies"] = self.db.getCurrencies()
        toSend["DetailedEvent"] = None

        return toSend

    def depositMoney(self,userID,currency,amount):
        self.db.depositMoney(userID,currency,int(amount))
        toSend = self.createDictWithDefaultInfo(userID)
        toSend['Message'] = "\n\nMoney deposited successfully!\n"
        
        return json.dumps(toSend)

    def withdrawMoney(self,userID,currency,amount):
        success = self.db.withdrawMoney(userID,currency,int(amount))
        toSend = self.createDictWithDefaultInfo(userID)

        if success:
            toSend['Message'] = "\n\nMoney withdrawn successfully!\n"

        else:
            toSend['Message'] = "\n\nNot enough money on wallet!\n"

        return json.dumps(toSend)

    def addBetToBetSlip(self,userID,eventID,result):
        print(f"User {userID} bet on event {eventID}, on {result}")

    def removeBetFromBetSlip(self,userID,eventID):
        print(f"User {userID} removed bett on event {eventID}")

    def getBetSlip(self,userID): # TODO: Create one if it does not exist
        betSlip = self.db.getBetSlip(userID)
        toSend = self.createDictWithDefaultInfo(userID)

        if betSlip == None:
            toSend['Exists'] = False
            toSend['Message'] = "\n\nError getting bet slip\n"
        
        else:
            toSend['Exists'] = True
            toSend['Message'] = "\n\nData Retrieved Successfully"
            toSend['Data'] = None # TODO

        return json.dumps(toSend)

    def cancelBetSlip(self,userID):
        print(f"User {userID} cancelled his bet slip")

    def concludeBetSlip(self,userID,amount,currency):
        print(f"Concluded Bet Slip")

    def getAvailableEvents(self,offset,numOfEvents):
        print(f"Presenting page {offset} with {numOfEvents} events")

    def getBetHistory(self,username):
        print("History retrieved!")

    def login(self,prevID,username,password):
        authenticated = self.db.authenticateUser(username,password)

        if not authenticated:
            toSend = self.createDictWithDefaultInfo(prevID)
            toSend['LoggedIn'] = False
            toSend['Message'] = "\n\nCould not login, check your credentials\n"
        
        else:
            toSend = self.createDictWithDefaultInfo(username)
            toSend['LoggedIn'] = True
            toSend['Message'] = f"\n\nAuthenticated! Welcome {username}!\n"

            del self.sessionsInfo[prevID]
            self.db.updateBetSlip(prevID,username)

        return json.dumps(toSend)

    def logout(self,username):
        toSend = self.createDictWithDefaultInfo(username)
        toSend['Message'] = "\n\nLogged out successfully\n"
        return json.dumps(toSend)

    def register(self,username,password,birthdate):
        toSend = self.createDictWithDefaultInfo(username)

        def age(birthdate : datetime.date):
            today = datetime.date.today()
            one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))
            year_difference = today.year - birthdate.year
            age = year_difference - one_or_zero
            return age
        
        date = datetime.datetime.strptime(birthdate,'%d/%m/%Y').date()
        age = age(date)

        if self.db.existsUser(username) or age < 18:

            print("Could not create user")
            toSend['Message'] = "\n\nCould not register user\n"
        else:
            self.db.createUser(username,password,birthdate)
            toSend['Message'] = "\n\nUser registered with success!\n"
            
        return json.dumps(toSend)

    def getCurrencies(self):
        return self.db.getCurrencies()

        
        

    


    
