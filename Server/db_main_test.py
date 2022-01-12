from Data.Database import Base, DataBase
from Data.DataClasses.Currency import Currency
from Data.DataClasses.User_Currency import User_Currency
from sqlalchemy_utils import database_exists, create_database
from Data.DataClasses.User import User
from Data.DataClasses.Event import Event
from Data.DataClasses.Sport import Sport, SportType
from Data.DataClasses.Intervenor import Intervenor
from Data.DataClasses.Intervenor_Event import Intervenor_Event
from Data.DataClasses.BetSlip import BetSlip
from Data.DataClasses.Bet import Bet
import datetime


def init_db():
    database = DataBase()

    Base.metadata.create_all(bind=database.engine)

    if not database_exists(database.engine.url):
            print("Creating database")
            database.create_database(database.engine.url)
    print("Creating tables")
    Base.metadata.create_all(database.engine)

    print("Initialized the db")

    #database.createDefault()
    user = database.getUser(1)
    user.password = "novapassword"
    database.session.commit()
    user2 = database.getUser(1)
    print(user2.password)
""" 
    new_sport = Sport(name="Futebol", type=SportType.WinDraw)
    new_intervenor = Intervenor(name="Intervenor1")
    new_intervenor_event = Intervenor_Event(intervenor=new_intervenor,odd=2.5)

    new_event = Event(name="Evento1",sport=new_sport,intervenors=[new_intervenor_event])
    new_currency = Currency(name="Escudos",value="420")
    new_user_currency = User_Currency(currency=new_currency,ammount=20)

    new_user = User(username="new_user",email="email@email.com",password="password1",wallet=[new_user_currency],messages="message1|message2", birthDate=datetime.date.today())
    new_betslip = BetSlip(user=new_user, amount=2.0, win_value=3.0,won=False)

    new_bet = Bet(betslip= new_betslip, event=new_event)

    database.addUser(new_user)

    retrieved_betslips = database.getUserBetslips(database.getUserByEmail(user_email="email@email.com").id)

    for betslip in retrieved_betslips:
        for bet in betslip.bets:
            print(bet.event.sport.name)
        print(str(betslip.win_value))
 """

if __name__ == "__main__":
    init_db()