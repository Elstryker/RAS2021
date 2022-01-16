from Data import DataBaseAccess
import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false

Base = declarative_base()

from Data.DataClasses.User import User
from Data.DataClasses.Event import Event, EventState
from Data.DataClasses.Sport import Sport, SportType
from Data.DataClasses.Intervenor import Intervenor
from Data.DataClasses.Intervenor_Event import Intervenor_Event
from Data.DataClasses.BetSlip import BetSlip, BetSlipState
from Data.DataClasses.Bet import Bet
from Data.DataClasses.Currency import Currency
from Data.DataClasses.User_Currency import User_Currency




""" class DataBase(): """
class DataBase(DataBaseAccess.DataBaseAccess):
    def __init__(self) -> None:
        self.engine = create_engine("mysql://admin:password@localhost/rasbetDB", connect_args= dict(host='localhost', port=3306))
        self.session = Session(self.engine)

    def createDefault(self):
        #criação de user e moeda

        dolar = self.createCurrency("dolar",1)
        euro = self.createCurrency("euro",1.12)

        user = self.createUser("ola","adeus","bit@connect",datetime.date(1970,1,1))

        self.depositMoney(user.username,dolar.name,25)
        self.depositMoney(user.username,euro.name,13.45)

        #criação de intervenientes e eventos
        futebol = self.createSport("Futebol",SportType.WinDraw)
        golf = self.createSport("Golf", SportType.Win)
        corrida = self.createSport("Corrida", SportType.Win)
        empate = self.createIntervenor("Draw")
        tiger = self.createIntervenor("Tiger Woods")
        jordan = self.createIntervenor("Jordan Spieth")
        rory = self.createIntervenor("Rory Mcllroy")
        naoko= self.createIntervenor("Naoko Takahashi")
        eliud = self.createIntervenor("Eliud Kipchoge")
        rosa = self.createIntervenor("Rosa Mota")
        porto = self.createIntervenor("FCPorto")
        barca = self.createIntervenor("FCBarcelona")
        braga = self.createIntervenor("SCBraga")

        e1 = self.createEventByObjects("Championship",futebol,[])
        e2 = self.createEventByObjects("Europa",futebol,[])
        e3 = self.createEventByObjects("Taça António Costa", golf,[])
        e4 = self.createEventByObjects("Torneio José Figueiras", corrida,[])

        self.createIntervenor_Event(porto,e1,1.05)
        empate_intervernor_event = self.createIntervenor_Event(empate,e1,6.21)
        self.createIntervenor_Event(braga,e1,1.50)
        porto_int_ev = self.createIntervenor_Event(porto,e2,1.56)
        self.createIntervenor_Event(empate,e2,3.67)
        self.createIntervenor_Event(barca,e2,2.00)
        self.createIntervenor_Event(tiger,e3,4.2)
        self.createIntervenor_Event(jordan,e3,2.3)
        self.createIntervenor_Event(rory,e3,.9)
        self.createIntervenor_Event(eliud,e4,4.2)
        self.createIntervenor_Event(naoko,e4,2.3)
        self.createIntervenor_Event(rosa,e4,8.1)

        #criação de bets

        betSlip1 = self.createBetSlipEmpty(user)
        #b1 = self.createBet(betSlip1,e1,empate,empate_intervernor_event.odd)
        b2 = self.createBet(betSlip1,e2,porto,porto_int_ev.odd)

        #betSlip1.addBet(b1)
        betSlip1.addBet(b2)
        self.concludeBetSlip(user.username, 25, "euro")


    def getUserHistory(self,username):
        user = self.getUserByUsername(username=username)
        return user.getHistory()

    def concludeBetSlip(self,username,amount,currency_name) -> None:
        betslip = self.getBetSlip(username)
        currency = self.getCurrency(currency_name)
        betslip.applyBetSlip(amount,currency)

        user = self.getUserByUsername(username=username)

        self.createBetSlipEmpty(user)


    def getCurrency(self, currency_name) -> Currency:
        currency = self.session.query(Currency)\
                           .filter(Currency.name == currency_name)\
                           .one_or_none()
        return currency

    #inacabado
    def updateBetSlip(self,prevID,username):
        curBetSlip = self.getBetSlipById(prevID)
        #numBets = len(curBetSlip.bets['Unfinished'])
        numBets = 0
        for bet in curBetSlip.bets:
            #if unfinished bet
                #numBets += 1
            pass
        
        if numBets == 0: # If no bets, get previous bet slip from user
            del self.betslips[prevID]
        else: # Replaces previous user bet slip with the current one
            self.betslips[username] = curBetSlip
            curBetSlip.user = username
            user = self.users[username]
            user.currentBetSlip = curBetSlip

    def getBetSlipById(self, betslipId):
        return self.session.query(BetSlip)\
                           .filter(BetSlip.id == betslipId)\
                           .one_or_none()

    def existsUser(self,username) -> bool:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        if user!=None:
            return True
        return False
    
    def createUser(self,name,password,email,birthDate):
        currencies = self.getCurrencies().values()
        user = User(name,password,email,birthDate)
        for currency in currencies:
            new_user_currency = User_Currency(user=user,currency=currency,amount=0)
            #user.wallet.append(new_user_currency)     
        self.addUser(user)
        return user

    def authenticateUser(self,username,password) -> bool:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        #print("got user " + user.username + " with password " + user.password)
        if user:
            if user.password == password:
                return True

        return False

    def getBetSlip(self, username) -> BetSlip:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        if user:
            betslip = self.session.query(BetSlip)\
                                  .filter(BetSlip.user_id == user.id , BetSlip.state==BetSlipState.Creating)\
                                  .one_or_none()
            print("Getting user " + username + " betslips")
            return betslip
        return None

    # se calhar queremos este metodo a devolver bool porque é um deposito?
    def depositMoney(self,username,currency,amount) -> None:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        currency = self.session.query(Currency)\
                               .filter(Currency.name == currency)\
                               .one_or_none()
        if user!=None and currency!=None:
            self.session.query(User_Currency)\
                        .filter(User_Currency.user_id == user.id , User_Currency.currency_id == currency.id)\
                        .update({User_Currency.amount: User_Currency.amount + amount})
            self.session.commit()

    def withdrawMoney(self,username,currency,amount) -> bool:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        currency = self.session.query(Currency)\
                               .filter(Currency.name == currency)\
                               .one_or_none()
        if user!=None and currency!=None:
            r = self.session.query(User_Currency)\
                        .filter(User_Currency.user_id == user.id, User_Currency.currency_id == currency.id, User_Currency.amount-amount >= 0)\
                        .update({User_Currency.amount: User_Currency.amount - amount})
            self.session.commit()
            # o update nao retorna nada por isso faço uma segunda consulta da mesma cena para ver se alterou o dinheiro (convém ver se há outra maneira)
            check = self.session.query(User_Currency)\
                                       .filter(User_Currency.user_id == user.id, User_Currency.currency_id == currency.id )\
                                       .one_or_none()
            if check!=None and check.amount >=0:
                return True
        return False

    def getUserWallet(self, username):
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        if user!=None:
            return self.session.query(User_Currency)\
                                               .filter(User_Currency.user_id == user.id)\
                                               .all()

    def getUserTotalBalance(self,username) -> dict:
        acc = {}
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        if user!=None:
            list_User_Currencies = self.session.query(User_Currency)\
                                               .filter(User_Currency.user_id == user.id)\
                                               .all()
            for user_currency in list_User_Currencies:
                currency = self.session.query(Currency)\
                                       .filter(Currency.id == user_currency.currency_id)\
                                       .one()
                acc.update({currency.name:user_currency.amount})
        return acc

    def getSuspendedEvents(self) -> list:
        event_list = self.session.query(Event)\
                                 .filter(Event.state == EventState.Suspended)\
                                 .all()
        return event_list

    def getAvailableEvents(self) -> list:
        event_list = self.session.query(Event)\
                                 .filter(Event.state == EventState.Open)\
                                 .all()
        return event_list

    # ? tf does this do
    def getParameters(self,obj):
        if obj == "Sport":
            return Sport.getParameters()
        elif obj == "Intervenor":
            return Intervenor.getParameters()
        elif obj == "Event":
            params = dict()
            
            params["Name"] = 0
            sports=[]
            q1 = self.getSports()
            for sport in q1:
                sports.append(sport.name)
            params["Sport"] = sports

            intervenors = []
            q2 = self.getIntervenors()
            for intervenor in q2:
                intervenors.append(intervenor.name)
            params["Intervenors"] = intervenors

            params["Odds"] = 0

            return params

    def getEvent(self,eventID) -> Event:
        event = self.session.query(Event)\
                           .filter(Event.id == eventID)\
                           .one_or_none()
        return event

    def addBetToBetSlip(self,username,eventID,result) -> bool:

        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()

        event = self.session.query(Event)\
                           .filter(Event.id == eventID)\
                           .one_or_none()
        
        betslip = self.session.query(BetSlip)\
                              .filter(BetSlip.user_id == user.id, BetSlip.state == BetSlipState.Creating)\
                              .one_or_none()
        intervenor_event = event.getIntervenorEventByIndex(result)
        
        previousBet = self.session.query(Bet)\
                              .filter(Bet.event_id == eventID, Bet.betslip_id == betslip.id)\
                              .one_or_none()

        if user and event!=None and betslip!=None and previousBet == None:
            bet = Bet(betslip,event,intervenor_event.intervenor,intervenor_event.odd)
            betslip.addBet(bet)
            self.session.commit()
            return True

        return False

    def removeBetFromBetSlip(self, username, eventID) -> bool:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()

        betslip = self.session.query(BetSlip)\
                              .filter(BetSlip.user_id == user.id, BetSlip.state == BetSlipState.Creating)\
                              .one_or_none()

        event = self.session.query(Event)\
                           .filter(Event.id == eventID)\
                           .one_or_none()

        if user and event and betslip:
            bet = self.session.query(Bet)\
                                .filter(Bet.event_id == eventID, Bet.betslip_id == betslip.id)\
                                .one_or_none()
            if bet:
                self.session.delete(bet)
                self.session.commit()
                return True


        return False


    def createSport(self, name, type: SportType):
        sport = Sport(type,name)
        self.addSport(sport)
        return sport

    def createIntervenor(self,name):
        intervenor = Intervenor(name)
        self.addIntervenor(intervenor)
        return intervenor

    def startEvent(self, eventID) -> bool:
        event = self.getEvent(eventID)
        if not event:
            return False
        if event.state != EventState.Open:
            return False

        event.initiateEvent()
        self.session.commit()
        return True

    def concludeEvent(self, eventID, result) -> None:
        event = self.getEvent(eventID)
        if not event:
            return False
        if event.state != EventState.Suspended:
            return False

        event.terminateEvent(result)
        self.session.commit()
        return True

        
    def getIntervenor(self, name):
        return self.session.query(Intervenor).filter(Intervenor.name == name).one_or_none()

    def createEvent(self, name, sportName, intervenors, odds) -> bool:
        eventSport = self.getSport(sportName)

        eventIntervenors = intervenors.split(",")
        eventOdds = odds.split(",")

        eventIntervenors = list(map(lambda x: self.getIntervenor(x),eventIntervenors))
        eventOdds = list(map(lambda x: float(x),eventOdds))

        nIntervenors = len(eventIntervenors)
        if (eventSport.type is SportType.WinDraw and nIntervenors != len(eventOdds)-1) or (eventSport.type is SportType.Win and nIntervenors != len(eventOdds)):
            return False
        if nIntervenors < 2:
            return False
        if eventSport.type is SportType.WinDraw and nIntervenors > 2:
            return False
        
        if eventSport.type is SportType.WinDraw:
            eventIntervenors.append(self.getIntervenor("Draw"))

        newEvent = self.createEventByObjects(name,eventSport,[])

        for i,intervenor in enumerate(eventIntervenors):
            self.createIntervenor_Event(intervenor,newEvent,eventOdds[i])

        return True


    def createEventByObjects(self,name,sport,intervenors_events):
        event = Event(name,sport,intervenors_events)
        self.addEvent(event)
        return event

    def createIntervenor_Event(self,intervenor,event,odd):
        intervenor_Event = Intervenor_Event(intervenor,event,odd)
        self.addIntervenor_Event(intervenor_Event)
        return intervenor_Event

    def getUsers(self):
        users = self.session.query(User).all()
        return users

    #creates currency and updates all user's wallets
    def createCurrency(self,name,value):
        currency = Currency(name,value)
        self.addCurrencyByObject(currency)
        users = self.getUsers()
        for user in users:
            self.createUser_Currency(user, currency,0)
        return currency

    def createUser_Currency(self,user,currency,amount):
        user_Currency = User_Currency(user,currency,amount)
        self.addUser_Currency(user_Currency)
        return user_Currency

    def createBetSlipEmpty(self, user):
        bet_slip = BetSlip(user)
        self.addBetSlip(bet_slip)
        return bet_slip
    
    def cancelBetSlip(self, username):
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()

        betslip = self.session.query(BetSlip)\
                              .filter(BetSlip.user_id == user.id, BetSlip.state == BetSlipState.Creating)\
                              .one_or_none()

        if user and betslip:
            for bet in betslip.bets:
                self.removeBetFromBetSlip(username,bet.event_id)
            self.session.delete(betslip)
            self.createBetSlipEmpty(user)
            self.session.commit()


        return False
    
    def createBetSlip(self,user,amount,win_value,won, currency):
        betSlip = BetSlip(user,amount,win_value,won, currency)
        self.addBetSlip(betSlip)
        return betSlip

    def createBet(self,betSlip,event,intervenor, odd):
        bet = Bet(betSlip,event,intervenor,odd)
        self.addBet(bet)

        return bet

    def addUser(self, user: User):
        """ try: """
        self.session.add(user)    
        self.session.commit() 
        """ except:
            print("Erro na inserção de User")
            self.session.rollback() """

    def addIntervenor(self, intervenor: Intervenor):
        try:
            self.session.add(intervenor)    
            self.session.commit() 
        except:
            print("Erro na inserção de Intervenor")
            self.session.rollback()

    def addEvent(self, event: Event):
        try:
            self.session.add(event)    
            self.session.commit() 
        except:
            print("Erro na inserção de Event")
            self.session.rollback()

    def addIntervenor_Event(self, intervenor_Event: Intervenor_Event):
        try:
            self.session.add(intervenor_Event)    
            self.session.commit() 
        except:
            print("Erro na inserção de Intervenor_Event")
            self.session.rollback()

    def currencyInBetSlips(self, currency):
        betslipsWithCurrency = self.session.query(BetSlip)\
                                  .filter(BetSlip.currency_id == currency.id)\
                                  .all()
        return len(betslipsWithCurrency) > 0

    #untested
    def removeCurrency(self, currencyName) -> None:
        currency = self.getCurrency(currencyName)
        print(f"removing currency {currency.name}")

        isUsedInBetSlip = self.currencyInBetSlips(currency)
        if (not isUsedInBetSlip) and currency:
            users = self.getUsers()
            for user in users:
                print(f"removing currency {currency.name} for user {user.username}")
                user_currencies = self.getUserWallet(user.username)
                for user_currency in user_currencies:
                    if user_currency.currency == currency:
                        new_amount = currency.convertToEUR(user_currency.amount)
                        self.withdrawMoney(user.username,currencyName,user_currency.amount)
                        self.depositMoney(user.username,"euro",new_amount)
                        self.session.delete(user_currency)

            self.session.delete(currency)

            self.session.commit()
        else:
            if currency:
                print(f"Some BetSlips use {currencyName}")

    def addCurrency(self, currencyName, toEUR) -> bool:
        return self.addCurrencyByObject(self.createCurrency(currencyName,toEUR))

    def addCurrencyByObject(self, currency: Currency):
        try:
            self.session.add(currency)    
            self.session.commit() 
            print(f"Added {currency.name} with {currency.id}")
            return True
        except:
            print("Erro na inserção de Currency")
            self.session.rollback()
            return False

    def addUser_Currency(self, user_currency: User_Currency):
        print(f"Added to user {user_currency.user.username}, currency {user_currency.currency.name} with amount {user_currency.amount}")
        self.session.add(user_currency)    
        self.session.commit() 
        

    def addBetSlip(self, new_betslip: BetSlip):
        try:
            self.session.add(new_betslip)
            self.session.commit()        
        except:
            print("Erro na inserção de Betslip")
            self.session.rollback()
       

    def addSport(self, new_sport: Sport):
        try:
            self.session.add(new_sport)
            print("Added sport " + str(new_sport.name)) 
        except:
            print("Erro na inserção de Sport")
            self.session.rollback()
        self.session.commit()  

    def addEvent(self, new_event: Event):
        try:
            self.session.add(new_event)
            print("Added Event " + str(new_event.name))
        except:
            print("Erro na inserção de Event")
            self.session.rollback()
        self.session.commit() 

    
    def addBet(self, bet: Bet):
        try:
            self.session.add(bet)
        except:
            print("Erro na inserção de Bet")
            self.session.rollback()
        self.session.commit()  


    
    def removeBet(self, bet: Bet):
        try:
            self.session.delete(bet)
        except:
            print("Erro na inserção de Bet")
            self.session.rollback()
        self.session.commit()  




    def getUser(self, user_id: Integer) -> User:
        user = self.session.query(User).filter(User.id == user_id).one()
        print(user.email)
        return user

    def getUserByEmail(self, user_email: str) -> User:
        user = self.session.query(User).filter(User.email == user_email).one()
        print(user.email)
        return user

    def getUserByUsername(self, username: str) -> User:
        user = self.session.query(User).filter(User.username == username).one_or_none()
        if user:
            print(user.username)
        return user
        
    def getUserBetslips(self, user_id: Integer):
        betslips = self.session.query(BetSlip).filter(BetSlip.user_id == user_id).all()
        print("Getting user id " + str(user_id) + " betslips")
        return betslips

    def getCurrencies(self) -> dict:
        ret_dict = {}
        currencies = self.session.query(Currency).all()
        for currency in currencies:
            ret_dict[currency.name] = currency
        return ret_dict

    def getIntervenors(self):
        intervenors = self.session.query(Intervenor).all()
        return intervenors

    def getSport(self, sportName):
        return self.session.query(Sport).filter(Sport.name == sportName).one_or_none()

    def getSports(self):
        sports = self.session.query(Sport).all()
        return sports
    
    def retrieveNotifications(self, username) -> list:
        user = self.getUserByUsername(username)
        if user != None:
            return user.retrieveNotifications()
        return []
            