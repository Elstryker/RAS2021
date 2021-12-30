from Data.DataClasses import BetSlip,User,Event,Bet,Intervenor,Sport
from Data import DataBaseAccess
from Data.DataClasses.Sport import SportType
class MemoryDataBase(DataBaseAccess.DataBaseAccess):

    currencies : list[str]
    users : dict[str,User.User] # username to user
    events : dict[int,dict[int,Event.Event]] # id to event
    bets : dict[int,Bet.Bet] # id to bet
    betslips : dict[str,BetSlip.BetSlip] # username to bet slip
    intervenors : dict[str,Intervenor.Intervenor] # name to intervenor
    sports : dict[str,Sport.Sport] # name to sport

    def __init__(self) -> None:
        self.currencies = ['EUR','USD','GBP','ADA']
        self.users = {}
        self.events = {"Available":dict(),"Suspended":dict(),"Ended":dict()}
        self.bets = {}
        self.betslips = {}
        self.intervenors = {}
        self.sports = {}
        # self.modified = 0 # Mudar quando há alterações
        self.createDefault()


    def createDefault(self):
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

    def getCurrencies(self):
        return self.currencies

    def existsUser(self,username):
        return username in self.users

    def createUser(self,username,password,birthdate):
        betSlip = BetSlip.BetSlip()
        user = User.User(username,password,self.currencies,birthdate,betSlip)
        self.betslips[user.username] = betSlip
        self.users[user.username] = user
        print(f"Created user {username} with betslip with id {betSlip.id}")

    def authenticateUser(self,username,password):
        ret = False
        if username in self.users:
            user = self.users[username]
            if user.password == password:
                ret = True
        return ret

    def updateBetSlip(self,prevID,username):
        curBetSlip = self.betslips[prevID]
        numBets = len(curBetSlip.bets['Unfinished'])
        if numBets == 0: # If no bets, get previous bet slip from user
            del self.betslips[prevID]
        else: # Replaces previous user bet slip with the current one
            self.betslips[username] = curBetSlip
            curBetSlip.user = username
            user = self.users[username]
            user.currentBetSlip = curBetSlip

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
        print(f"Deposited {amount} {currency}. Total: {user.wallet[currency]}")

    def withdrawMoney(self,username,currency,amount):
        user = self.users[username]
        if user.wallet[currency] < amount:
            print(f"Yo u don't have all that, only {user.wallet[currency]} {currency}")
            return False
        else:
            user.wallet[currency] -= amount
            print(f"You're rich m8, there you have it, total: {user.wallet[currency]} {currency}")
            return True

    def getUserTotalBalance(self,username):
        if username in self.users:
            user = self.users[username]
            return dict(user.wallet) # Copy so the values in DB are not changed by Business Logic
        else:
            return 0

    def getAvailableEvents(self,page,eventsPerPage):
        availableEvents = self.events["Available"]
        availableEvents = availableEvents.values()

        if len(availableEvents) < (page * eventsPerPage):
            page -= 1
        
        availableEvents = sorted(availableEvents,key=lambda x: x.id)
        returnEvents = availableEvents[page*eventsPerPage:(page+1)*eventsPerPage]

        return (returnEvents,page)


    

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
        oddsWithIntervenors.append((eventOdds[-1],None))
        newEvent = Event.Event(name,eventSport,oddsWithIntervenors)
        self.events["Available"][newEvent.id] = newEvent
        return True
        
        
