from Data import Event, DataBaseAccess

class MemoryDataBase(DataBaseAccess.DataBaseAccess):  # Colocar a interface aqui
    
    def __init__(self) -> None:
        self.eventos = Event.Event()
