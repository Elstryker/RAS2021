class ClientGUI:

    @staticmethod
    def showMenu():
        print(
"""
0 -> Quit
1 -> Add Bet To Bet Slip
2 -> Remove Bet From Bet Slip
3 -> Cancel Bet Slip
4 -> Show Bet Slip
5 -> Deposit Money
6 -> Withdraw Money
7 -> Previous Page
8 -> Next Page
9 -> Login""")

    def askAmount():
        print(
"""
Amount:""")

    def askCurrency(availableCurrencies):
        print(
"""
Choose currency:""")
        for i,el in enumerate(availableCurrencies):
            print(f"{i+1} - {el}")
