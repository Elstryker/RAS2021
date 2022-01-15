from Data.DataClasses import BetSlip,User,Event,Bet,Intervenor,Sport,Currency
from Data import DataBaseAccess
from Data.DataClasses.Sport import SportType
class MemoryDataBase(DataBaseAccess.DataBaseAccess):

    currencies : dict[str,Currency.Currency]
    users : dict[str,User.User] # username to user
    events : dict[int,dict[int,Event.Event]] # id to event
    bets : dict[int,Bet.Bet] # id to bet
    betslips : dict[str,BetSlip.BetSlip] # username to bet slip
    intervenors : dict[str,Intervenor.Intervenor] # name to intervenor
    sports : dict[str,Sport.Sport] # name to sport

    def __init__(self) -> None:
        self.currencies = {}
        self.users = {}
        self.events = {"Available":dict(),"Suspended":dict(),"Ended":dict()}
        self.bets = {}
        self.betslips = {}
        self.intervenors = {}
        self.sports = {}
        # self.modified = 0 # Mudar quando há alterações
        self.createDefault()


    def createDefault(self):
        self.currencies = {'EUR':Currency.Currency('EUR',1), 'USD':Currency.Currency('USD',0.84), 'GBP':Currency.Currency('GBP',1.20), 'ADA':Currency.Currency('ADA',1.03)}
        self.createUser("ola","adeus","1/1/1970")
        self.createSport("Futebol",SportType.WinDraw)
        self.createSport("Golf", SportType.Win)
        self.createSport("Corrida", SportType.Win)

        self.createIntervenor("Tiger Woods")
        self.createIntervenor("Jordan Spieth")
        self.createIntervenor("Rory Mcllroy")
        self.createIntervenor("Naoko Takahashi")
        self.createIntervenor("Eliud Kipchoge")
        self.createIntervenor("Rosa Mota")
        self.createIntervenor("FCPorto")
        self.createIntervenor("FCBarcelona")
        self.createIntervenor("SCBraga")

        self.createEvent("Championship","Futebol","FCPorto,SCBraga","1.05,6.21,1.50")
        self.createEvent("Europa","Futebol","FCPorto,FCBarcelona","1.56,3.67,2.00")
        self.createEvent("Taça António Costa", "Golf", "Tiger Woods,Jordan Spieth,Rory Mcllroy", "4.2, 2.3, 1.9")
        self.createEvent("Torneio José Figueiras", "Corrida", "Eliud Kipchoge,Naoko Takahashi,Rosa Mota", "4.2, 2.3, 8.1")

        self.addBetToBetSlip("ola",3,1)
        self.depositMoney("ola","EUR",20)

        print(self.betslips)

        for event in self.events["Available"].values():
            print(f"{event.id} - {event.name}")

    def getCurrencies(self):
        return self.currencies

    def existsUser(self,username):
        return username in self.users

    def createUser(self,username,password,birthdate):
        betSlip = BetSlip.BetSlip()
        user = User.User(username,password,self.currencies,birthdate,betSlip)
        betSlip.user = user.username
        betSlip.attach(user)
        self.betslips[user.username] = betSlip
        self.users[user.username] = user

    def authenticateUser(self,username,password):
        ret = False
        if username in self.users:
            user = self.users[username]
            if user.password == password:
                ret = True
        return ret

    def getBetSlip(self,username):
        if username in self.betslips:
            return self.betslips[username]
        else:
            newBetSlip = BetSlip.BetSlip()
            newBetSlip.user = username
            self.betslips[username] = newBetSlip
            return None

    def depositMoney(self,username,currency,amount):
        user = self.users[username]
        user.wallet[currency] += amount

    def withdrawMoney(self,username,currency,amount):
        user = self.users[username]
        if user.wallet[currency] < amount:
            return False
        else:
            user.wallet[currency] -= amount
            return True

    def getUserTotalBalance(self,username):
        if username in self.users:
            user = self.users[username]
            return dict(user.wallet) # Copy so the values in DB are not changed by Business Logic
        else:
            return 0

    def getAvailableEvents(self):
        availableEvents = self.events["Available"]
        availableEvents = availableEvents.values()
        
        availableEvents = sorted(availableEvents,key=lambda x: x.id)

        return availableEvents
    

    def getParameters(self,obj):
        if obj == "Sport":
            return Sport.Sport.getParameters()
        elif obj == "Intervenor":
            return Intervenor.Intervenor.getParameters()
        elif obj == "Event":
            params = dict()
            
            params["Name"] = 0

            sports = list(self.sports.keys())
            params["Sport"] = sports

            intervenors = list(self.intervenors.keys())
            params["Intervenors"] = intervenors

            params["Odds"] = 0

            return params



    def createSport(self,name,type):
        newSport = Sport.Sport(type,name)
        if newSport.name not in self.sports:
            self.sports[newSport.name] = newSport
            return True
        
        return False
        
    def createIntervenor(self,name):
        newIntervenor = Intervenor.Intervenor(name)
        if newIntervenor.name not in self.intervenors:
            self.intervenors[newIntervenor.name] = newIntervenor
            return True
        
        return False

    def createEvent(self,name,sport,intervenors,odds):
        eventSport = self.sports[sport]
        eventIntervenors = intervenors.split(",")
        eventOdds = odds.split(",")

        eventIntervenors = list(map(lambda x: self.intervenors[x],eventIntervenors))
        eventOdds = list(map(lambda x: float(x),eventOdds))

        nIntervenors = len(eventIntervenors)
        if (eventSport.type is SportType.WinDraw and nIntervenors != len(eventOdds)-1) or (eventSport.type is SportType.Win and nIntervenors != len(eventOdds)):
            return False
        if nIntervenors < 2:
            return False
        if eventSport.type is SportType.WinDraw and nIntervenors > 2:
            return False
        
        oddsWithIntervenors = list(zip(eventOdds,eventIntervenors))

        if eventSport.type is SportType.WinDraw:
            oddsWithIntervenors.append((eventOdds[-1],None))
        
        newEvent = Event.Event(name,eventSport,oddsWithIntervenors)
        self.events["Available"][newEvent.id] = newEvent
        return True
        
    def getEvent(self,eventID):
        try:
            event = self.events["Available"][eventID]
            return event
        except:
            return None

        
    def addBetToBetSlip(self,username,eventID,result):
        event = self.events["Available"][eventID]
        betslip = self.betslips[username]

        event.attach(betslip)

        if result >= len(event.intervenors):
            return False
        
        newBet = Bet.Bet(result,event.getOdd(result),event,betslip.id)
        self.bets[newBet.id] = newBet

        betslip.addBet(newBet)

        return True
        
    def removeBetFromBetSlip(self,username,eventID):
        betslip = self.betslips[username]

        return betslip.removeBet(eventID)

    def cancelBetSlip(self,username):
        betslip = self.betslips[username]
        betslip.cancel()

    def concludeBetSlip(self,username,amount,currency) -> None:
        betslip = self.betslips[username]
        betslip.applyBetSlip(amount,currency)

        user = self.users[username]

        newBetSlip = BetSlip.BetSlip()
        newBetSlip.user = user.username
        newBetSlip.attach(user)
        self.betslips[user.username] = newBetSlip

        user.concludeBetSlip(newBetSlip)

    def getUserHistory(self,username):
        user = self.users[username]
        return list(user.betSlips.values())

    def addCurrency(self,currency,toEUR):
        if currency in self.currencies:
            return False

        self.currencies[currency] = Currency.Currency(currency,toEUR)

        for user in self.users.values():
            user.wallet[currency] = 0

        return True

    def removeCurrency(self,currency):
        curr = self.currencies.pop(currency)
        
        for user in self.users.values():
            amount = user.wallet.pop(currency)
            amount = curr.convertToEUR(amount)
            user.wallet["EUR"] += amount

    def startEvent(self,eventID):
        if eventID not in self.events["Available"]:
            return False

        event = self.events["Available"].pop(eventID)
        event.initiateEvent()
        self.events["Suspended"][eventID] = event

        return True

    def getSuspendedEvents(self):
        suspendedEvents = self.events["Suspended"]
        suspendedEvents = suspendedEvents.values()
        
        suspendedEvents = sorted(suspendedEvents,key=lambda x: x.id)

        return suspendedEvents

    def concludeEvent(self,eventID,result):
        event = self.events["Suspended"].pop(eventID)
        event.terminateEvent(result)
        self.events["Ended"][eventID] = event

    def retrieveNotifications(self,username):
        if username in self.users:
            user = self.users[username]
            return user.retrieveNotifications()

        print("Not retrieved!")
        return []