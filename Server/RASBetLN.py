
import RASBetFacade
from Data import DataBaseAccess
import datetime, json

class RASBetLN(RASBetFacade.RASBetFacade):

    db : DataBaseAccess.DataBaseAccess

    def __init__(self,db : DataBaseAccess.DataBaseAccess) -> None:
        self.db = db

    def createDictWithDefaultInfo(self,userID):

        def convertNotification(notification):
            tokens = notification.split(" ")
            if tokens[0] == "Won":
                return (1,(float(tokens[1]),tokens[2]))
            else:
                return (0,None)

        toSend = dict()
        toSend["Wallet"] = self.db.getUserTotalBalance(userID)
        events = self.db.getAvailableEvents()
        toSend["Events"] = [x.toJSON() for x in events]
        toSend["Currencies"] = list(self.db.getCurrencies().keys())
        
        notifs = self.db.retrieveNotifications(userID)
        toSend["Notifications"] = [convertNotification(x) for x in notifs]

        return toSend

    def depositMoney(self,userID,currency,amount):
        self.db.depositMoney(userID,currency,float(amount))
        toSend = self.createDictWithDefaultInfo(userID)
        toSend['Message'] = "\n\nMoney deposited successfully!\n"
        
        return json.dumps(toSend)

    def withdrawMoney(self,userID,currency,amount):
        success = self.db.withdrawMoney(userID,currency,float(amount))
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
        amount = float(amount)
        success = self.db.withdrawMoney(userID,currency,amount)

        toSend = self.createDictWithDefaultInfo(userID)
        if not success:
            toSend["Success"] = False
            toSend["Message"] = "\n\nNot enough funds\n"
            return json.dumps(toSend)
        
        success = self.db.concludeBetSlip(userID,amount,currency)
        if not success:
            toSend["Success"] = False
            toSend["Message"] = "\n\nAn event in your betslip is no longer open\n"
            return json.dumps(toSend)

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

    def login(self,username,password,prevBetSlip):
        authenticated = self.db.authenticateUser(username,password)

        if not authenticated:
            toSend = self.createDictWithDefaultInfo(None)
            toSend['LoggedIn'] = False
            toSend['Message'] = "\n\nCould not login, check your credentials\n"
        
        else:
            toSend = self.createDictWithDefaultInfo(username)
            toSend['LoggedIn'] = True
            toSend['Message'] = f"\n\nAuthenticated! Welcome {username}!\n"
            # "0" if prevBetSlip has no bets or formatted like -> "1,2:3,1:2,1" with ":" as bet separator and (eventID,result)
            if prevBetSlip != "0":
                bets = prevBetSlip.split(":")
                betSlip = [x.split(",") for x in bets]

                self.db.cancelBetSlip(username)
                
                for eventID,result in betSlip:
                    self.db.addBetToBetSlip(username,int(eventID),int(result))

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

    def startEvent(self,eventID):
        toSend = dict()
        eventID = int(eventID)
        success = self.db.startEvent(eventID)

        if success:
            toSend["Message"] = "\n\nStarted event"

        else:
            toSend["Message"] = "\n\nCould not start event"

        return json.dumps(toSend)


    def concludeEvent(self,args):
        toSend = dict()
        if args[0] == "GET":
            events = self.db.getSuspendedEvents()
            events = [x.toJSON() for x in events]
            toSend["Events"] = events
        
        else:
            eventID = int(args[1])
            result = int(args[2])
            self.db.concludeEvent(eventID,result)
            toSend["Message"] = "\n\nEvent terminated\n"

        return json.dumps(toSend)

    def addCurrency(self,currency,toEUR):
        toSend = dict()
        toEUR = float(toEUR)
        success = self.db.addCurrency(currency,toEUR)
        if success:
            toSend["Message"] = "\n\nCurrency added\n"

        else:
            toSend["Message"] = "\n\nCould not add currency\n"

        return json.dumps(toSend)

    def removeCurrency(self, currency):
        toSend = dict()
        currencies = self.db.getCurrencies()

        if currency in currencies:
            self.db.removeCurrency(currency)
            toSend["Message"] = "\n\nCurrency removed successfully\n"
        
        else:
            toSend["Message"] = "\n\nCould not remove currency\n"

        return json.dumps(toSend)


        

    


    
