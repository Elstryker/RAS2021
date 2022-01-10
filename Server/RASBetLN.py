import RASBetFacade
from Data import DataBaseAccess
import datetime, json

class RASBetLN(RASBetFacade.RASBetFacade):

    db : DataBaseAccess.DataBaseAccess

    def __init__(self,db : DataBaseAccess.DataBaseAccess) -> None:
        self.db = db

    def createDictWithDefaultInfo(self,userID):
        toSend = dict()
        toSend["Wallet"] = self.db.getUserTotalBalance(userID)
        events = self.db.getAvailableEvents()
        toSend["Events"] = list(map(lambda x:x.toJSON(),events))
        toSend["Currencies"] = list(self.db.getCurrencies().keys())

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
            toSend["Success"] = True

        else:
            toSend['Message'] = "\n\nNot enough money on wallet!\n"
            toSend["Success"] = False

        return json.dumps(toSend)

    def addBetToBetSlip(self,userID,args): # args -> "GET",eventID  ||  "PUT",eventID,result
        toSend = self.createDictWithDefaultInfo(userID)
        eventID = int(args[1])

        if args[0] == "GET":
            event = self.db.getEvent(eventID)
            if event is None:
                toSend["Success"] = False
                toSend["Message"] = "Could not get event"
            else:
                toSend["Success"] = True
                toSend["Event"] = event.toJSON()
                toSend["Message"] = "Retrieved event"
        elif args[0] == "PUT":
            result = int(args[2])
            success = self.db.addBetToBetSlip(userID,eventID,result)
            toSend = self.createDictWithDefaultInfo(userID)
            if success:
                toSend["Message"] = "Bet added to bet slip"
                toSend["Success"] = True
            else:
                toSend["Message"] = "Problem adding bet to bet slip"
                toSend["Success"] = False
        else:
            print("WTF, this is not supposed to happen")

        return json.dumps(toSend)
        

    def removeBetFromBetSlip(self,userID,eventID):
        eventID = int(eventID)

        success = self.db.removeBetFromBetSlip(userID,eventID)
        toSend = self.createDictWithDefaultInfo(userID)
        if success:
            toSend["Message"] = "Bet removed successfully"
            toSend["Success"] = True
        else:
            toSend["Message"] = "Could not remove bet"
            toSend["Success"] = False

        return json.dumps(toSend)

    def getBetSlip(self,userID): # TODO: Create one if it does not exist
        betSlip = self.db.getBetSlip(userID)
        toSend = self.createDictWithDefaultInfo(userID)

        if betSlip == None:
            toSend['Success'] = False
            toSend['Message'] = "\n\nError getting bet slip\n"
        
        else:
            toSend['Success'] = True
            toSend['Message'] = "\n\nData Retrieved Successfully"
            toSend['BetSlip'] = betSlip.toJSON()

        return json.dumps(toSend)

    def cancelBetSlip(self,userID):
        self.db.cancelBetSlip(userID)

        toSend = self.createDictWithDefaultInfo(userID)

        toSend["Message"] = "\n\nCancelled bet slip\n"

        return json.dumps(toSend)

    def concludeBetSlip(self,userID,amount,currency):
        amount = int(amount)
        success = self.db.withdrawMoney(userID,currency,amount)

        toSend = self.createDictWithDefaultInfo(userID)
        if not success:
            toSend["Success"] = False
            toSend["Message"] = "\n\nNot enough funds\n"
            return json.dumps(toSend)
        
        self.db.concludeBetSlip(userID,amount,currency)

        toSend["Success"] = True
        toSend["Message"] = "\n\nBet slip concluded\n"

        return json.dumps(toSend)


    def getBetHistory(self,username):
        toSend = self.createDictWithDefaultInfo(username)

        history = self.db.getUserHistory(username)
        history.sort(key=lambda x:x.id)

        toSend["History"] = [x.toJSON() for x in history]
        toSend["Message"] = "\n\nHistory retrieved\n"

        return json.dumps(toSend)

    def exchangeMoney(self,userID,fromCur,toCur,amount):
        currencies = self.db.getCurrencies()
        fromCurrency = currencies[fromCur]
        toCurrency = currencies[toCur]
        amount = int(amount)

        success = self.db.withdrawMoney(userID,fromCur,amount)
        if not success:
            toSend = self.createDictWithDefaultInfo(userID)
            toSend["Success"] = False
            toSend["Message"] = "\n\nInvalid amount\n"

            return json.dumps(toSend)
        
        totalEUR = fromCurrency.convertToEUR(amount)
        total = toCurrency.convertFromEUR(totalEUR)

        self.db.depositMoney(userID,toCur,total)
        
        toSend = self.createDictWithDefaultInfo(userID)
        toSend["Success"] = True
        toSend["Message"] = "\n\nExchange complete\n"

        return json.dumps(toSend)

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
            toSend["Success"] = False
        else:
            self.db.createUser(username,password,birthdate)
            toSend['Message'] = "\n\nUser registered with success!\n"
            toSend["Success"] = True
            
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
        

    


    
