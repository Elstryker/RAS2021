import time
from os import name
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.layout import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.pretty import pprint

class ClientGUI:
    console : Console
    questions : list

    def __init__(self):
        self.console = Console()
        self.questions = list()
        self.questions.append(Text("""
  _____       _                 _                          _    _                                              
 |_   _|     | |               | |                        | |  | |                                           _ 
   | |  _ __ | |_ _ __ ___   __| |_   _ ______ _    ___   | |  | |___  ___ _ __ _ __   __ _ _ __ ___   ___  (_)
   | | | '_ \| __| '__/ _ \ / _` | | | |_  / _` |  / _ \  | |  | / __|/ _ \ '__| '_ \ / _` | '_ ` _ \ / _ \    
  _| |_| | | | |_| | | (_) | (_| | |_| |/ / (_| | | (_) | | |__| \__ \  __/ |  | | | | (_| | | | | | |  __/  _ 
 |_____|_| |_|\__|_|  \___/ \__,_|\__,_/___\__,_|  \___/   \____/|___/\___|_|  |_| |_|\__,_|_| |_| |_|\___| (_)                                                                                                                                                                                                                           
                    """))
        self.questions.append(Text("""
  _____       _                 _                          _____                                    _     
 |_   _|     | |               | |                        |  __ \                                  | |  _ 
   | |  _ __ | |_ _ __ ___   __| |_   _ ______ _    __ _  | |__) |_ _ ___ _____      _____  _ __ __| | (_)
   | | | '_ \| __| '__/ _ \ / _` | | | |_  / _` |  / _` | |  ___/ _` / __/ __\ \ /\ / / _ \| '__/ _` |    
  _| |_| | | | |_| | | (_) | (_| | |_| |/ / (_| | | (_| | | |  | (_| \__ \__ \\\ V  V / (_) | | | (_| |  _ 
 |_____|_| |_|\__|_|  \___/ \__,_|\__,_/___\__,_|  \__,_| |_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_| (_)
                                                                                                          
                                                                                                          
"""))
        self.questions.append(Text("""
  _____        _              _                             _                      _           __   _     _     __                      __                   __      
 |  __ \      | |            | |                           (_)                    | |         / /  | |   | |   / /                     / /                   \ \   _ 
 | |  | | __ _| |_ __ _    __| | ___   _ __   __ _ ___  ___ _ _ __ ___   ___ _ __ | |_ ___   | | __| | __| |  / / __ ___  _ __ ___    / /_ _  __ _  __ _  __ _| | (_)
 | |  | |/ _` | __/ _` |  / _` |/ _ \ | '_ \ / _` / __|/ __| | '_ ` _ \ / _ \ '_ \| __/ _ \  | |/ _` |/ _` | / / '_ ` _ \| '_ ` _ \  / / _` |/ _` |/ _` |/ _` | |    
 | |__| | (_| | || (_| | | (_| |  __/ | | | | (_| \__ \ (__| | | | | | |  __/ | | | || (_) | | | (_| | (_| |/ /| | | | | | | | | | |/ / (_| | (_| | (_| | (_| | |  _ 
 |_____/ \__,_|\__\__,_|  \__,_|\___| |_| |_|\__,_|___/\___|_|_| |_| |_|\___|_| |_|\__\___/  | |\__,_|\__,_/_/ |_| |_| |_|_| |_| |_/_/ \__,_|\__,_|\__,_|\__,_| | (_)
                                                                                              \_\                                                            /_/     
                                                                                                                                                                     
"""))

    def goodbye(self):
        layout : Layout = Layout()
        
        goodbye_text = Text("""
   ____  _          _                 _                                                _ _                
  / __ \| |        (_)               | |                                              | | |               
 | |  | | |__  _ __ _  __ _  __ _  __| | ___    _ __   ___  _ __    ___  ___  ___ ___ | | |__   ___ _ __  
 | |  | | '_ \| '__| |/ _` |/ _` |/ _` |/ _ \  | '_ \ / _ \| '__|  / _ \/ __|/ __/ _ \| | '_ \ / _ \ '__| 
 | |__| | |_) | |  | | (_| | (_| | (_| | (_) | | |_) | (_) | |    |  __/\__ \ (_| (_) | | | | |  __/ |    
  \____/|_.__/|_|  |_|\__, |\__,_|\__,_|\___/  | .__/ \___/|_|     \___||___/\___\___/|_|_| |_|\___|_|    
                       __/ |    _____          | |_____ ____  ______ _______                              
                      |___/    |  __ \     /\  |_/ ____|  _ \|  ____|__   __|                             
                               | |__) |   /  \  | (___ | |_) | |__     | |                                
                               |  _  /   / /\ \  \___ \|  _ <|  __|    | |                                
                               | | \ \  / ____ \ ____) | |_) | |____   | |                                
                               |_|  \_\/_/    \_\_____/|____/|______|  |_|                                
                                                                                                          
                                                                                                          
""")
        goodbye_text.stylize("bold yellow")

        layout.split_column(
            Layout(" ", name="empty space", ratio=3),
            Layout(Align(goodbye_text, align='center'), ratio=3)
        )

        self.console.print(layout)


    def ask_info(self, events : list, question : int):
        answer = ''
        eventos_printable : list = self.showEvents(events)
        prompt = self.questions[question]
                
        prompt.stylize("bold yellow")                                                                                       
                                                                                                           

        while answer == '':
            self.console.clear()
            layout : Layout = Layout()
        
            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(eventos_printable, title='[red]Eventos'), name="events", ratio=9),
                Layout(prompt, ratio=3)
            )

            self.login_layout(False, layout)

            self.console.print(layout)
            answer = self.console.input("-> ")
        return answer
    
    def login_layout(self, loggedIn : bool, layout : Layout):
        logo_panel = self.get_logo_panel()

        if loggedIn:
            layout["header"].split_row(
                Layout(logo_panel, name='logo', ratio = 8), 
                Layout(" ", ratio=2),
                Layout(" ", name='balance', ratio = 1)
            )
        else:
            
            wallet : dict = {"EUR" : 42, "USD" : 69, "GBP" : 666, "ADA" : 420, "RASCoin" : 0}
            wallet_printable : str = ""
            
            for currency, amount in wallet.items():
                wallet_printable+= f'{currency}: {amount}\n'

            balance_panel = Panel(Align(Text(wallet_printable, justify='center'), vertical='middle', align='center'), title='[red]Saldo')

            
            layout["header"].split_row(
                Layout(logo_panel, name='logo', ratio = 8),
                Layout(name="login", ratio=2),
                Layout(balance_panel, name='balance', ratio = 1)
            )

            layout["login"].split_column(
                Layout(" "),
                Layout(Panel(Align(Text("Joaquim das Couves", justify='center'),vertical='middle', align='center'), title='[red]Username'))
            )

    def get_logo_panel(self):
        rasbet_logo = Text("""
    ______  ___   ___________      _   
    | ___ \/ _ \ /  ___| ___ \    | |  
    | |_/ / /_\ \\\ `--.| |_/ / ___| |_ 
    |    /|  _  | `--. \ ___ \/ _ \ __|
    | |\ \| | | |/\__/ / |_/ /  __/ |_ 
    \_| \_\_| |_/\____/\____/ \___|\__|
    """)                                   
        rasbet_logo.stylize("bold yellow")                                   

        logo_panel = Align(rasbet_logo, vertical='middle', align='center')

        return logo_panel

    def showMenu(self, loggedIn : bool, wallet : dict[str,int], events : list):
        self.console.clear()
        layout : Layout = Layout()
        
        

        """
        2 -> Remove Bet From Bet Slip
        3 -> Cancel Bet Slip
        4 -> Show Bet Slip
        5 -> Previous Page
        6 -> Next Page
        7 -> Login
        8 -> Register"""
        
        if not loggedIn:
            menu = [Panel("[red]E[/red]fetuar registo"), Panel("[red]F[/red]azer Login"), 
            Panel("[red]I[/red]ntroduzir Aposta"), Panel("[red]R[/red]emover Aposta"), 
            Panel("[red]C[/red]ancelar Boletim"), Panel("[red]M[/red]ostrar Boletim"), 
            Panel("[red]V[/red]alidar Boletim"), Panel("[red]D[/red]epositar Dinheiro"), 
            Panel("[red]L[/red]evantar Dinheiro"), Panel("Página [red]A[/red]nterior"), 
            Panel("[red]P[/red]róxima Página"), Panel("[red]S[/red]air")]
        else:
            menu = Text(
    """
    0 -> Quit
    1 -> Add Bet To Bet Slip
    2 -> Remove Bet From Bet Slip
    3 -> Cancel Bet Slip
    4 -> Show Bet Slip
    5 -> Conclude Bet Slip
    6 -> Deposit Money
    7 -> Withdraw Money
    8 -> Previous Page
    9 -> Next Page
    10 -> See Bet History
    11 -> Logout""", justify = 'center')

        menu_printable = Columns(menu, equal=True, expand=True)

        eventos_printable : list = self.showEvents(events)
        
        
        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Eventos'), name="events", ratio=9),
            Layout(Panel(menu_printable, title='[red]Menu'), name="menu", ratio=3)
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("Introduza a inicial da opção desejada -> ")

        #time.sleep(2)
        #console.clear()

    def askAmount(self):
        print(
    """
    Amount:""")

    def askCurrency(self, availableCurrencies):
        print(
    """
    Choose currency:""")
        for i,el in enumerate(availableCurrencies):
            print(f"{i+1} - {el}")

    def askEvent(self):
        print("Which event?")

    def showDetailedEvent(self):
        print(
    """
    0 - Empate
    1 - Vitória
    2 - Derrota
    """)

    
    def showEvents(self, events : list):
        eventos_formatted = []
        
        for event in events:
            table_painel = Table()
            table_painel.add_column(Text(event["Sport"]["Name"], justify='center'))

            table = Table()

            table_painel.add_row(Text(event["Name"], justify='center'))

            intervenors = [x[1] for x in event["Intervenors"]]
            odds = [str(x[0]) for x in event["Intervenors"]]
            table.add_column(intervenors[0], justify="center", style="green", no_wrap=True)
                
            if event["Sport"]["Type"] == "WinDraw":
                intervenors.remove("Draw")
                drawOdd = odds.pop(-1)
                odds.insert(1,drawOdd)
                table.add_column("vs", justify="center", style="yellow", no_wrap=True)
                table.add_column(intervenors[1], justify="center", style="green", no_wrap=True)     
            else:
                table.add_column(intervenors[1], justify="center", style="green", no_wrap=True)
                table.add_column(intervenors[2], justify="center", style="green", no_wrap=True)     
            
            
            table.add_row(Text(odds[0], justify="center"), odds[1], odds[2])

            table_painel.add_row(table)

            eventos_formatted.append(table_painel)
            #string = " vs ".join(intervenors)
            #print(string)
            #string = " ; ".join(odds)
            #print(string)
            #print("______________________________")
        return Columns(eventos_formatted, equal=False, expand=True, align='center')