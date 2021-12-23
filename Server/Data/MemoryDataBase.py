from Data import DataBaseAccess,BetSlip,User
import datetime
class MemoryDataBase(DataBaseAccess.DataBaseAccess):

    def __init__(self) -> None:
        self.currencies = ['Euros','Dollars','English_pounds','Cardans']
        self.users = {}
        self.events = {}
        self.bets = {}
        self.betslips = {}
        self.intervenors = {}
        self.sports = {}

    def getCurrencies(self):
        return self.currencies

    def createUser(self,username,password,birthdate):

        def age(birthdate : datetime.date):
            today = datetime.date.today()
            one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))
            year_difference = today.year - birthdate.year
            age = year_difference - one_or_zero
            return age
        
        date = datetime.datetime.strptime(birthdate,'%d/%m/%Y').date()
        age = age(date)

        if username in self.users or age < 18:
            print("Could not create user")
            return False
        else:
            betSlip = BetSlip.BetSlip()
            self.betslips[betSlip.id] = betSlip
            user = User.User(username,password,self.currencies,birthdate,betSlip)
            self.users[user.username] = user
            print(f"Created user {username} with betslip with id {betSlip.id}")
            return True 