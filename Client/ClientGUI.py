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
    username : str
    wallet : dict

    def __init__(self):
        self.console = Console()
        self.username = None
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
  _| |_| | | | |_| | | (_) | (_| | |_| |/ / (_| | | (_| | | |  | (_| \__ \__ \\ V  V / (_) | | | (_| |  _ 
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
        self.questions.append(Text("""
  _____           _                     __  __             _              _           
 |_   _|         (_)                   |  \/  |           | |            | |        _ 
   | |  _ __  ___ _ _ __ __ _    ___   | \  / | ___  _ __ | |_ __ _ _ __ | |_ ___  (_)
   | | | '_ \/ __| | '__/ _` |  / _ \  | |\/| |/ _ \| '_ \| __/ _` | '_ \| __/ _ \    
  _| |_| | | \__ \ | | | (_| | | (_) | | |  | | (_) | | | | || (_| | | | | ||  __/  _ 
 |_____|_| |_|___/_|_|  \__,_|  \___/  |_|  |_|\___/|_| |_|\__\__,_|_| |_|\__\___| (_)
                                                                                      
                                                                                      
"""))
        self.questions.append(Text("""
 _____      _                 _                                               _              _                _           _           
|_   _|    | |               | |                                             | |            | |              (_)         | |        _ 
  | | _ __ | |_ _ __ ___   __| |_   _ ______ _    ___     _____   _____ _ __ | |_ ___     __| | ___  ___  ___ _  __ _  __| | ___   (_)
  | || '_ \| __| '__/ _ \ / _` | | | |_  / _` |  / _ \   / _ \ \ / / _ \ '_ \| __/ _ \   / _` |/ _ \/ __|/ _ \ |/ _` |/ _` |/ _ \     
 _| || | | | |_| | | (_) | (_| | |_| |/ / (_| | | (_) | |  __/\ V /  __/ | | | || (_) | | (_| |  __/\__ \  __/ | (_| | (_| | (_) |  _ 
 \___/_| |_|\__|_|  \___/ \__,_|\__,_/___\__,_|  \___/   \___| \_/ \___|_| |_|\__\___/   \__,_|\___||___/\___| |\__,_|\__,_|\___/  (_)
                                                                                                            _/ |                      
                                                                                                           |__/                       
"""))

        self.questions.append(Text("""
  _____                   _                                       _                          _            _           
 |  __ \                 (_)                                     | |                        | |          | |        _ 
 | |__) | __ ___  ___ ___ _  ___  _ __   ___     __ _ _   _  __ _| | __ _ _   _  ___ _ __   | |_ ___  ___| | __ _  (_)
 |  ___/ '__/ _ \/ __/ __| |/ _ \| '_ \ / _ \   / _` | | | |/ _` | |/ _` | | | |/ _ \ '__|  | __/ _ \/ __| |/ _` |    
 | |   | | |  __/\__ \__ \ | (_) | | | |  __/  | (_| | |_| | (_| | | (_| | |_| |  __/ |     | ||  __/ (__| | (_| |  _ 
 |_|   |_|  \___||___/___/_|\___/|_| |_|\___|   \__, |\__,_|\__,_|_|\__, |\__,_|\___|_|      \__\___|\___|_|\__,_| (_)
                                                   | |                 | |                                            
                                                   |_|                 |_|                                            
"""))
        self.questions.append(Text("""
 _____          _                     ___________       _                               _            
|_   _|        (_)                   |_   _|  _  \     | |                             | |         _ 
  | | _ __  ___ _ _ __ __ _    ___     | | | | | |   __| | __ _    __ _ _ __   ___  ___| |_ __ _  (_)
  | || '_ \/ __| | '__/ _` |  / _ \    | | | | | |  / _` |/ _` |  / _` | '_ \ / _ \/ __| __/ _` |    
 _| || | | \__ \ | | | (_| | | (_) |  _| |_| |/ /  | (_| | (_| | | (_| | |_) | (_) \__ \ || (_| |  _ 
 \___/_| |_|___/_|_|  \__,_|  \___/   \___/|___/    \__,_|\__,_|  \__,_| .__/ \___/|___/\__\__,_| (_)
                                                                       | |                           
                                                                       |_|                           
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

    def invalid_info(self, opcao : int):
            self.console.clear()
            mensagem = list()

            mensagem.append(self.questions[5])
            mensagem.append(Text("""
  ______                _                 _                             __                      
 |  ____|              | |               (_)                           / _|                     
 | |__ __ _  ___ __ _  | |     ___   __ _ _ _ __    _ __   ___  _ __  | |_ __ ___   _____  _ __ 
 |  __/ _` |/ __/ _` | | |    / _ \ / _` | | '_ \  | '_ \ / _ \| '__| |  _/ _` \ \ / / _ \| '__|
 | | | (_| | (_| (_| | | |___| (_) | (_| | | | | | | |_) | (_) | |    | || (_| |\ V / (_) | |   
 |_|  \__,_|\___\__,_| |______\___/ \__, |_|_| |_| | .__/ \___/|_|    |_| \__,_| \_/ \___/|_|   
             )_)                     __/ |         | |                                          
                                    |___/          |_|                                          
"""))

            mensagem.append(Text("""
   _____            _               _____             __  _ _     _                
  |  __ \          | |             |_   _|           /_/ | (_)   | |               
  | |  | | __ _  __| | ___  ___      | |  _ ____   ____ _| |_  __| | ___  ___      
  | |  | |/ _` |/ _` |/ _ \/ __|     | | | '_ \ \ / / _` | | |/ _` |/ _ \/ __|     
  | |__| | (_| | (_| | (_) \__ \    _| |_| | | \ V / (_| | | | (_| | (_) \__ \     
  |_____/ \__,_|\__,_|\___/|___/   |_____|_| |_|\_/ \__,_|_|_|\__,_|\___/|___/     
   _______         _                                                       _       
  |__   __|       | |                                                     | |      
     | | ___ _ __ | |_ ___      _ __   _____   ____ _ _ __ ___   ___ _ __ | |_ ___ 
     | |/ _ \ '_ \| __/ _ \    | '_ \ / _ \ \ / / _` | '_ ` _ \ / _ \ '_ \| __/ _ \\
     | |  __/ | | | ||  __/    | | | | (_) \ V / (_| | | | | | |  __/ | | | ||  __/
     |_|\___|_| |_|\__\___|    |_| |_|\___/ \_/ \__,_|_| |_| |_|\___|_| |_|\__\___|
                                                                                   
                                                                                   
"""))
            for elem in mensagem:
                elem.stylize("bold red")
                                                                              

            layout : Layout = Layout()

            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(Align(mensagem[opcao], align='center', vertical="middle")), ratio=9),
                Layout(mensagem[0], ratio=3)
            )

            self.login_layout(False, layout)

            self.console.print(layout)
            answer = self.console.input("-> ")

    def show_betslip(self, ):
        self.console.clear()
        layout : Layout = Layout()

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

        return self.console.input("Introduza a letra da opção desejada -> ")

    def ask_info(self, loggedIn : bool, events : list, question : int):
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

            self.login_layout(loggedIn, layout)

            self.console.print(layout)
            answer = self.console.input("-> ")
        return answer
    
    def login_layout(self, loggedIn : bool, layout : Layout):
        logo_panel = self.get_logo_panel()

        if not loggedIn:
            layout["header"].split_row(
                Layout(logo_panel, name='logo', ratio = 8), 
                Layout(" ", ratio=2),
                Layout(" ", name='balance', ratio = 1)
            )
        else:
            
            wallet : dict = {"EUR" : 42, "USD" : 69, "GBP" : 666, "ADA" : 420, "RASCoin" : 0}
            wallet_printable : str = ""
            
            for currency, amount in self.wallet.items():
                wallet_printable+= f'{currency}: {amount}\n'

            balance_panel = Panel(Align(Text(wallet_printable, justify='center'), vertical='middle', align='center'), title='[red]Saldo')

            
            layout["header"].split_row(
                Layout(logo_panel, name='logo', ratio = 8),
                Layout(name="login", ratio=2),
                Layout(balance_panel, name='balance', ratio = 1)
            )

            
            logout = Text("Logout", justify='center')
            logout.stylize("red", 1,2)

            layout["login"].split_column(
                Layout(Panel(Align(logout,vertical='middle', align='center'))),
                Layout(Panel(Align(Text(self.username, justify='center'),vertical='middle', align='center'), title='[red]Username'))
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

    

    def pede_moeda(self, events : list, currencies : list, conclude : bool):
        self.console.clear()
        layout : Layout = Layout()
        
        currencies = [Panel(Align(Text(currency, tab_size=8), align='center'), title=f'[red]{index}[/red]') for index,currency in enumerate(currencies)]

        moedas_printable = Columns(currencies, equal=False, expand=True)
        
        if conclude:
            eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
            
            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
                Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(events["BetSlip"]['MultipliedOdd']), align='center')),
                Layout(Panel(moedas_printable, title='[red]Menu'), name="menu", ratio=3)
            )
        else:    
            eventos_printable : list = self.showEvents(events)
            
            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(eventos_printable, title='[red]Eventos'), name="events", ratio=9),
                Layout(Panel(moedas_printable, title='[red]Menu'), name="menu", ratio=3)
            )
        
        

        self.login_layout(True, layout)

        self.console.print(layout)

        return self.console.input("Introduza o número da opção desejada -> ")
 

    def show_betslip(self, events, opcao):
        self.console.clear()

        layout : Layout = Layout()

        prompt = self.questions[opcao]
        prompt.stylize("bold yellow")

        eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
        
        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
            Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(events["BetSlip"]['MultipliedOdd']), align='center')),
            Layout(Align(prompt, align='center'), name="menu", ratio=3)
        )

        self.login_layout(True, layout)

        self.console.print(layout)

        return self.console.input("->")

    def showMenu(self, loggedIn : bool, wallet : dict[str,int], events : list):
        self.console.clear()
        layout : Layout = Layout()
        
        if not loggedIn:
            menu = [Panel("[red]E[/red]fetuar registo"), Panel("[red]F[/red]azer Login"), 
            Panel("[red]I[/red]ntroduzir Aposta"), Panel("[red]R[/red]emover Aposta"), 
            Panel("[red]C[/red]ancelar Boletim"), Panel("[red]M[/red]ostrar Boletim"), 
            Panel("[red]V[/red]alidar Boletim"), Panel("Página [red]A[/red]nterior"), 
            Panel("[red]P[/red]róxima Página"), Panel("[red]S[/red]air")]
        else:
            menu = [Panel("[red]I[/red]ntroduzir Aposta"), Panel("[red]R[/red]emover Aposta"), 
            Panel("[red]C[/red]ancelar Boletim"), Panel("[red]M[/red]ostrar Boletim"), 
            Panel("[red]V[/red]alidar Boletim"), Panel("[red]D[/red]epositar Dinheiro"), 
            Panel("[red]L[/red]evantar Dinheiro"), Panel("Página [red]A[/red]nterior"), 
            Panel("[red]P[/red]róxima Página"), Panel("Consultar [red]H[/red]istórico"), 
            Panel("Co[red]n[/red]verter Moeda"), Panel("[red]S[/red]air")]

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

        return self.console.input("Introduza a letra da opção desejada -> ")


    def conclude_betslip(self, loggedIn, events):
        self.console.clear()

        if loggedIn:
            layout : Layout = Layout()

            prompt = Text("""
     _   _       _ _     _             ______       _      _   _          ___    _____    ___   _ 
    | | | |     | (_)   | |            | ___ \     | |    | | (_)        |__ \  /  ___|  / / \ | |
    | | | | __ _| |_  __| | __ _ _ __  | |_/ / ___ | | ___| |_ _ _ __ ___   ) | \ `--.  / /|  \| |
    | | | |/ _` | | |/ _` |/ _` | '__| | ___ \/ _ \| |/ _ \ __| | '_ ` _ \ / /   `--. \/ / | . ` |
    \ \_/ / (_| | | | (_| | (_| | |    | |_/ / (_) | |  __/ |_| | | | | | |_|   /\__/ / /  | |\  |
     \___/ \__,_|_|_|\__,_|\__,_|_|    \____/ \___/|_|\___|\__|_|_| |_| |_(_)   \____/_/   \_| \_/
                                                                                                
                                                                                                
    """)
            prompt.stylize("bold yellow")

            eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
            
            layout.split_column(
                Layout(" ", name="empty space"),
                Layout(name="header", ratio=3),
                Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
                Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(events["BetSlip"]['MultipliedOdd']), align='center')),
                Layout(Align(prompt, align='center'), name="menu", ratio=3)
            )

            self.login_layout(True, layout)

            self.console.print(layout)

            resposta = self.console.input("->")

        else:
            self.invalid_info(1)
            resposta = "N"

        return resposta 

    def ask_amount(self, events):
        self.console.clear()

        layout : Layout = Layout()
        prompt = self.questions[3]
        prompt.stylize("bold yellow")

        eventos_printable : list = self.showEventsSlip(events["BetSlip"]['Bets'])
        
        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Boletim'), name="events", ratio=8),
            Layout(Align("[bold yellow] ODD FINAL:[/bold yellow] " + str(events["BetSlip"]['MultipliedOdd']), align='center')),
            Layout(Align(prompt, align='center'), name="menu", ratio=3)
        )

        self.login_layout(True, layout)

        self.console.print(layout)

        return self.console.input("->")
        
    def showDetailedEvent(self, loggedIn, eventos,event):
        self.console.clear()
        layout : Layout = Layout()
        participants : list = list()

        print(f'evento: {event["Sport"]["Type"]}')
        
        if event["Sport"]["Type"] == "WinDraw":
            participants.append(Panel(f"[bold yellow]{event['Intervenors'][0][0]}[/] -- {event['Intervenors'][0][1]}", title=f"[red]{0}[/red]"))
            participants.append(Panel(f"[bold yellow]{event['Intervenors'][2][0]}[/] -- {event['Intervenors'][2][1]}", title=f"[red]{1}[/red]"))
            participants.append(Panel(f"[bold yellow]{event['Intervenors'][1][0]}[/] -- {event['Intervenors'][1][1]}", title=f"[red]{2}[/red]"))
        else:
            for i,(odd,intervenor) in enumerate(event["Intervenors"]):
                participants.append(Panel(f"[bold yellow]{odd}[/] -- {intervenor}", title=f"[red]{i}[/red]"))

        participants_printable = Columns(participants, equal=True, expand=True, align='center')


        eventos_printable : list = self.showEvents(eventos)
        
        opcoes_layout : Layout = Layout()

        opcoes_layout.split_column(
            Layout(Text(event["Name"], justify='center'), ratio=2),
            Layout(participants_printable, ratio=3)
        )

        opcoes : Layout = Layout(Panel(opcoes_layout, title=f'[red]{event["Sport"]["Name"]}[/red]'), name="menu", ratio=3)

        layout.split_column(
            Layout(" ", name="empty space"),
            Layout(name="header", ratio=3),
            Layout(Panel(eventos_printable, title='[red]Eventos'), name="events", ratio=9),
            opcoes
        )

        self.login_layout(loggedIn, layout)

        self.console.print(layout)

        return self.console.input("Introduza o número da aposta desejada -> ")

    def showEventsSlip(self, events : list):
        eventos_formatted = []
        
        for event in events:
            table_painel =  Table()
            texto = Text(str(event["EventID"]) + " | " + event["EventName"], justify='center')
            texto.stylize("red", 0, 2)
            table_painel.add_column(texto)
            
            table = Table()

            table.add_column(str("Aposta"), justify="center", style="cyan", no_wrap=True)
            table.add_column(str("Odd"), justify="center", style="bold yellow", no_wrap=True)
            
            
            table.add_row(str(event["Choice"]), str(event["Odd"]))

            table_painel.add_row(table)

            eventos_formatted.append(table_painel)
        

        return Columns(eventos_formatted, equal=False, align='center')

    def showEvents(self, events : list):
        eventos_formatted = []
        
        for event in events:
            
            table_painel = Table()
            texto = Text(str(event["Id"]) + " | " + event["Sport"]["Name"], justify='center')
            texto.stylize("bold red", 0, 2)
            table_painel.add_column(texto)

            table = Table()

            table_painel.add_row(Text(event['Name'], justify='center'))

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
       
        return Columns(eventos_formatted, equal=False, expand=True, align='center')