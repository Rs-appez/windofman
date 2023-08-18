
import PySimpleGUI as sg

class WindowConfig():

    def __init__(self) -> None:
        
        self.window = sg.Window(title="Windofman", layout=[[]], margins=(600, 100))

    def start(self):
        while 1 :
            event,values = self.window.read()
            if event ==sg.WIN_CLOSED:
                break
        self.window.close()
