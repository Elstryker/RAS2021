def showMenu():
    print(
"""
0 -> Quit
1 -> Add Event
2 -> Add Sport
3 -> Add Intervenor
4 -> Start Event
5 -> Conclude Event
6 -> Add Currency
7 -> Remove Currency
8 -> Update Currency Exchange Value""")

def askParam(param):
    print(f"{param}: ")

def askLimitedParam(paramName,param,chooseMultiple = False):
    if chooseMultiple:
        print(f"{paramName} (format: option1,option2,...):")
    else:
        print(f"{paramName}:")
    for i,el in enumerate(param):
        print(f"{i+1} - {el}")

def printEvents(events):
    for i,event in enumerate(events):
        print(f"{i} - {event['Name']}")
