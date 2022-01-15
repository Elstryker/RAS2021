#import DataBaseAccess
from datetime import date
import datetime
from enum import unique
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



""" class DataBase(DataBaseAccess.DataBaseAccess): """
class DataBase():

    def __init__(self) -> None:

        self.engine = create_engine("mysql://admin:password@localhost/rasbetDB", connect_args= dict(host='localhost', port=3306))
        self.session = Session(self.engine)

    def createDefault(self):

        #criação de user e moeda
        user = self.createUser("ola","adeus","bit@connect",datetime.date(1970,1,1))

        dolar = self.createCurrency("dolar",1)
        euro = self.createCurrency("euro",1.12)

        self.createUser_Currency(user,dolar,25)
        self.createUser_Currency(user,euro,13.45)

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

        e1 = self.createEvent("Championship",futebol,[])
        e2 = self.createEvent("Europa",futebol,[])
        e3 = self.createEvent("Taça António Costa", golf,[])
        e4 = self.createEvent("Torneio José Figueiras", corrida,[])

        self.createIntervenor_Event(porto,e1,1.05)
        self.createIntervenor_Event(empate,e1,6.21)
        self.createIntervenor_Event(braga,e1,1.50)
        self.createIntervenor_Event(porto,e2,1.56)
        self.createIntervenor_Event(empate,e2,3.67)
        self.createIntervenor_Event(barca,e2,2.00)
        self.createIntervenor_Event(tiger,e3,4.2)
        self.createIntervenor_Event(jordan,e3,2.3)
        self.createIntervenor_Event(rory,e3,.9)
        self.createIntervenor_Event(eliud,e4,4.2)
        self.createIntervenor_Event(naoko,e4,2.3)
        self.createIntervenor_Event(rosa,e4,8.1)

        #criação de bets

        betSlip1 = self.createBetSlip(user,5,5,False,euro)

        b1 = self.createBet(betSlip1,e1,empate)
        self.createBet(betSlip1,e2,porto)

        self.removeBet(b1)

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
        currencies = self.getCurrencies()
        user = User(name,password,email,birthDate)
        wallet_list = []
        for currency in currencies:
            new_user_currency = User_Currency(user=user,currency=currency,amount=0)        
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
                                  .all()
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

    def getAvailableEvents(self,page,eventsPerPage) -> list:
        acc = []
        event_list = self.session.query(Event)\
                                 .filter(Event.state == EventState.Open)\
                                 .all()
        start = page*eventsPerPage
        end = (page+1)*eventsPerPage
        i=0
        for event in event_list:
            if start<=i and end>i:
                acc.append(event)
            i+=1
        return (acc,page)

    # ? tf does this do
    def getParameters(self,obj):
        if obj == "Sport":
            return Sport.Sport.getParameters()
        elif obj == "Intervenor":
            return Intervenor.Intervenor.getParameters()
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

    #por testar acho que nao precisamos deste metodo, quando criamos a bet já é ligada automaticamente ao betslip correspondente
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

        if event!=None and betslip!=None:
            bet = Bet(betslip,event)
            self.addBet(bet)
        return False


    def createSport(self, name, type: SportType):
        sport = Sport(type,name)
        self.addSport(sport)
        return sport

    def createIntervenor(self,name):
        intervenor = Intervenor(name)
        self.addIntervenor(intervenor)
        return intervenor

    def createEvent(self,name,sport,intervenors_events):
        event = Event(name,sport,intervenors_events)
        self.addEvent(event)
        return event

    def createIntervenor_Event(self,intervenor,event,odd):
        intervenor_Event = Intervenor_Event(intervenor,event,odd)
        self.addIntervenor_Event(intervenor_Event)
        return intervenor_Event

    def createCurrency(self,name,value):
        currency = Currency(name,value)
        self.addCurrency(currency)
        return currency

    def createUser_Currency(self,user,currency,amount):
        user_Currency = User_Currency(user,currency,amount)
        self.addUser_Currency(user_Currency)
        return user_Currency

    
    def createBetSlip(self,user,amount,win_value,won, currency):
        betSlip = BetSlip(user,amount,win_value,won, currency)
        self.addBetSlip(betSlip)
        return betSlip

    def createBet(self,betSlip,event,intervenor):
        bet = Bet(betSlip,event,intervenor)
        self.addBet(bet)

        return bet

    def addUser(self, user: User):
        try:
            self.session.add(user)    
            self.session.commit() 
        except:
            print("Erro na inserção de User")
            self.session.rollback()

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

    def addCurrency(self, currency: Currency):
        try:
            self.session.add(currency)    
            self.session.commit() 
        except:
            print("Erro na inserção de Currency")
            self.session.rollback()

    def addUser_Currency(self, user_currency: User_Currency):
        try:
            self.session.add(user_currency)    
            self.session.commit() 
        except:
            print("Erro na inserção de User_Currency")
            self.session.rollback()

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
        
    def getUserBetslips(self, user_id: Integer):
        betslips = self.session.query(BetSlip).filter(BetSlip.user_id == user_id).all()
        print("Getting user id " + str(user_id) + " betslips")
        return betslips

    def getCurrencies(self):
        currencies = self.session.query(Currency).all()
        return currencies


    def getIntervenors(self):
        intervenors = self.session.query(Intervenor).all()
        return intervenors


    def getSports(self):
        sports = self.session.query(Sports).all()
        return sports