class ClientInfo:
    
    availableCurrencies : list

    def __init__(self,availableCurrencies) -> None:
        self.loggedIn = False
        self.wallet = {}
        self.availableCurrencies = availableCurrencies

    def updateInfo(self,info):
        pass