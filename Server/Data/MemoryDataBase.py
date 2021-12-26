from Data.DataClasses import BetSlip,User,Event,Bet,Intervenor,Sport
from Data import DataBaseAccess
class MemoryDataBase(DataBaseAccess.DataBaseAccess):

    currencies : list[str]
    users : dict[str,User.User]
    events : dict[str,dict[int,Event.Event]]
    bets : dict[int,Bet.Bet]
    betslips : dict[str,BetSlip.BetSlip]
    intervenors : dict[str,Intervenor.Intervenor]
    sports : dict[str,Sport.Sport]

    def __init__(self) -> None:
        self.currencies = ['Euros','Dollars','English Pounds','Cardans']
        self.users = {}
        self.events = {"Available":dict(),"Suspended":dict(),"Ended":dict()}
        self.bets = {}
        self.betslips = {}
        self.intervenors = {}
        self.sports = {}
        self.createDefault()

    def createDefault(self):
        self.createUser("ola","adeus","1/1/1970")

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

    def getAvailableEvents(self,page,eventsPerPage): # TODO
        availableEvents = self.events["Available"]
        availableEvents = availableEvents.values()

        if len(availableEvents) > (page * eventsPerPage):
            availableEvents = sorted(availableEvents,key=lambda x: x.id)
            returnEvents = availableEvents[page*eventsPerPage:(page+1)*eventsPerPage]


        
        
