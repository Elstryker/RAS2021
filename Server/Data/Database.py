#import DataBaseAccess
from datetime import date
import datetime
from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false

Base = declarative_base()

from DataClasses.User import User
from DataClasses.Event import Event, EventState
from DataClasses.Sport import Sport, SportType
from DataClasses.Intervenor import Intervenor
from DataClasses.Intervenor_Event import Intervenor_Event
from DataClasses.BetSlip import BetSlip, BetSlipState
from DataClasses.Bet import Bet
from DataClasses.Currency import Currency
from DataClasses.User_Currency import User_Currency



""" class DataBase(DataBaseAccess.DataBaseAccess): """
class DataBase():

    def __init__(self) -> None:

        self.engine = create_engine("mysql://admin:password@localhost/rasbetDB", connect_args= dict(host='localhost', port=3306))
        self.session = Session(self.engine)

    def createDefault(self):
        self.createUser("ola","adeus","bit@connect",datetime.date(1970,1,1))
        futebol = self.createSport("Futebol",SportType.WinDraw)
        golf = self.createSport("Golf", SportType.Win)
        corrida = self.createSport("Corrida", SportType.Win)

        empate = self.createIntervenor("Empate")
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

    def existsUser(self,username) -> bool:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        if user!=None:
            return True
        return False
    
    def createUser(self,name,password,email,birthDate):
        currencies = self.getCurrencies()
        wallet_list = []
        for currency in currencies:
            new_user_currency = User_Currency(currency=currency,amount=0)
            wallet_list.append(new_user_currency)
        user = User(name,password,email,birthDate,wallet_list)
        self.addUser(user)
        return user

    #por testar
    def authenticateUser(self,username,password) -> bool:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        if user!=None:
            if user.password == password:
                return True

        return False

    #por testar
    def getBetslip(self, username) -> BetSlip.BetSlip:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        if user:
            betslip = self.session.query(BetSlip)\
                                  .filter(BetSlip.user_id == user.id & BetSlip.state==BetSlipState.Creating)\
                                  .all()
            print("Getting user " + username + " betslips")
            return betslip
        return None

    #por testar
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
                        .filter(User_Currency.user_id == user.id & User_Currency.currency_id == currency.id)\
                        .update({User_Currency.amount: User_Currency.amount + amount})

    #por testar
    def withdrawMoney(self,username,currency,amount) -> bool:
        user = self.session.query(User)\
                           .filter(User.username == username)\
                           .one_or_none()
        currency = self.session.query(Currency)\
                               .filter(Currency.name == currency)\
                               .one_or_none()
        if user!=None and currency!=None:
            self.session.query(User_Currency)\
                        .filter(User_Currency.user_id == user.id & User_Currency.currency_id == currency.id & User_Currency.amount-amount >= 0)\
                        .update({User_Currency.amount: User_Currency.amount - amount})

            # o update nao retorna nada por isso faço uma segunda consulta da mesma cena para ver se alterou o dinheiro (convém ver se há outra maneira)
            check = self.session.query(User_Currency)\
                                       .filter(User_Currency.user_id == user.id & User_Currency.currency_id == currency.id )\
                                       .one_or_none()
            if check!=None and check.amount-amount >=0:
                return True
        return False

    #por testar
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

    
    #por testar
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
        return acc

    # ? tf does this do
    def getParameters(self,obj) -> dict:
        pass


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

    #por testar
    def getEvent(self,eventID) -> Event.Event:
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
                              .filter(BetSlip.user_id == user.id & BetSlip.state == BetSlipState.Creating)\
                              .one_or_none()

        if event!=None and betslip!=None:
            bet = Bet(betslip,event)
            self.addBet(bet)
        return False


    def addUser(self, user: User):
        self.session.add(user)    
        self.session.commit() 
        """ try:
            self.session.add(user)    
            self.session.commit() 
            print("Added user " +  user.username)
        except:
            print("Erro na inserção de User")
            self.session.rollback() """
        
    

    def addIntervenor(self, intervenor: Intervenor):

        self.session.add(intervenor)    
        self.session.commit() 
        """ try:
            self.session.add(intervenor)    
            self.session.commit() 
        except:
            print("Erro na inserção de Intervenor")
            self.session.rollback() """

    def addEvent(self, event: Event):

        self.session.add(event)    
        self.session.commit()
        """ try:
            self.session.add(event)    
            self.session.commit() 
        except:
            print("Erro na inserção de Event")
            self.session.rollback() """

    def createIntervenor_Event(self, intervenor, event, odd):
        intervenor_Event = Intervenor_Event(intervenor, event, odd)
        self.addIntervenor_Event(intervenor_Event)

    def addIntervenor_Event(self, intervenor_Event: Intervenor_Event):
        self.session.add(intervenor_Event)    
        self.session.commit() 
        """ try:
            self.session.add(intervenor_Event)    
            self.session.commit() 
        except:
            print("Erro na inserção de Intervenor_Event")
            self.session.rollback()
 """

    def addBetSlip(self, new_betslip: BetSlip):
        try:
            self.session.add(new_betslip)
            print("Added betslip " + str(new_betslip.winValue))
        except:
            print("Erro na inserção de Betslip")
            self.session.rollback()
        self.session.commit()        
       

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


    """ def addCurrency(self, currency: Currency):
        try:
            self.session.add(currency)    
            self.session.commit() 
            print("Added currency " +  currency.name)
        except:
            print("Erro na inserção de Currency")
            self.session.rollback() """