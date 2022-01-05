#import DataBaseAccess
from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from DataClasses.User import User
from DataClasses.Event import Event
from DataClasses.Sport import Sport, SportType
from DataClasses.Intervenor import Intervenor
from DataClasses.Intervenor_Event import Intervenor_Event
from DataClasses.BetSlip import BetSlip
from DataClasses.Bet import Bet

""" class DataBase(DataBaseAccess.DataBaseAccess): """
class DataBase():

    def __init__(self) -> None:

        self.engine = create_engine("mysql://admin:password@localhost/rasbetDB", connect_args= dict(host='localhost', port=3306))
        self.session = Session(self.engine)

    def addUser(self, user: User):
        try:
            self.session.add(user)    
            self.session.commit() 
            print("Added user " +  user.username)
        except:
            print("Erro na inserção de User")
            self.session.rollback()
        

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

