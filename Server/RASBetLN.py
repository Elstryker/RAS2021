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

        sessionInfo = self.sessionsInfo[userID]
        toSend = dict()
        toSend["Wallet"] = self.db.getUserTotalBalance(userID)
        events = self.db.getAvailableEvents(sessionInfo["Page"],sessionInfo["EventsPerPage"])
        self.sessionsInfo[userID]["Page"] = events[1]
        toSend["Events"] = list(map(lambda x:x.toJSON(),events[0]))
        toSend["Currencies"] = self.db.getCurrencies()

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

    def addBetToBetSlip(self,userID,args): # args -> "GET",eventID  ||  "PUT",eventID,result
        toSend = self.createDictWithDefaultInfo(userID)
        eventID = int(args[1])

        if args[0] == "GET":
            event = self.db.getEvent(eventID)
            if event is None:
                toSend["Found"] = False
                toSend["Message"] = "Could not get event"
            else:
                toSend["Found"] = True
                toSend["Event"] = event.toJSON()
                toSend["Message"] = "Retrieved event"
        elif args[0] == "PUT":
            result = int(args[2])
            success = self.db.addBetToBetSlip(userID,eventID,result)
            if success:
                toSend["Message"] = "Bet added to bet slip"
            else:
                toSend["Message"] = "Problem adding bet to bet slip"
        else:
            print("WTF, this is not supposed to happen")

        return json.dumps(toSend)
        

    def removeBetFromBetSlip(self,userID,eventID):
        toSend = self.createDictWithDefaultInfo(userID)
        eventID = int(eventID)

        success = self.db.removeBetFromBetSlip(userID,eventID)
        if success:
            toSend["Message"] = "Bet removed successfully"
        else:
            toSend["Message"] = "Could not remove bet"

        return json.dumps(toSend)

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

    def getDefaultInfo(self,userID):
        return json.dumps(self.createDictWithDefaultInfo(userID))


    # ---------------------------------------- Bookie Methods ---------------------------------------- #
        
    def addEvent(self,args):
        toSend = dict()
        if args[0] == "GET":
            toSend["Params"] = self.db.getParameters("Event")
        
        else:
            if self.db.createEvent(args[1],args[2],args[3],args[4]):
                toSend["Message"] = "\n\nEvent added\n"
            else:
                toSend["Message"] = "\n\nCould not add Event\n"

        return json.dumps(toSend)

    def addSport(self,args):
        toSend = dict()
        if args[0] == "GET":
            toSend["Params"] = self.db.getParameters("Sport")
        
        else:
            if self.db.createSport(args[1],args[2]):
                toSend["Message"] = "\n\nSport added\n"
            else:
                toSend["Message"] = "\n\nCould not add Sport\n"

        return json.dumps(toSend)

    def addIntervenor(self,args):
        toSend = dict()
        if args[0] == "GET":
            toSend["Params"] = self.db.getParameters("Intervenor")
        
        else:
            if self.db.createIntervenor(args[1]):
                toSend["Message"] = "\n\nIntervenor added\n"
            else:
                toSend["Message"] = "\n\nCould not add Intervenor\n"

        return json.dumps(toSend)

    def startEvent(self,args):
        pass

    def concludeEvent(self,args):
        pass
        

    


    
