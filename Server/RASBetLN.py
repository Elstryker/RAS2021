import RASBetFacade
from Data import DataBaseAccess
import datetime, json

class RASBetLN(RASBetFacade.RASBetFacade):
    # TODO: Have memory structure to have client session data for correct continuous data fetching

    db : DataBaseAccess.DataBaseAccess

    def __init__(self,db : DataBaseAccess.DataBaseAccess) -> None:
        self.db = db

    def depositMoney(self,userID,currency,amount):
        self.db.depositMoney(userID,currency,int(amount))
        toSend = dict()
        toSend['Message'] = "\n\nMoney deposited successfully!\n"
        
        return json.dumps(toSend)

    def withdrawMoney(self,userID,currency,amount):
        success = self.db.withdrawMoney(userID,currency,int(amount))
        toSend = dict()

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
        toSend = dict()

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

    def getEvents(self,offset,numOfEvents):
        print(f"Presenting page {offset} with {numOfEvents} events")

    def getBetHistory(self,username):
        print("History retrieved!")

    def login(self,prevID,username,password):
        toSend = dict()
        authenticated = self.db.authenticateUser(username,password)

        if not authenticated:
            toSend['LoggedIn'] = False
            toSend['Message'] = "\n\nCould not login, check your credentials\n"
        
        else:
            toSend['LoggedIn'] = True
            toSend['Message'] = f"\n\nAuthenticated! Welcome {username}!\n"

            self.db.updateBetSlip(prevID,username)

        return json.dumps(toSend)

    def logout(self):
        toSend = dict()
        toSend['Message'] = "\n\nLogged out successfully\n"
        return json.dumps(toSend)

    def register(self,username,password,birthdate):
        toSend = dict()

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

        
        

    


    
