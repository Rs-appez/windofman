from pynput import keyboard
from windowManager import WindowManager
import threading

class KeyboardManager():

    def __init__(self,windowManager : WindowManager):
        self.alt_pressed = False
        self.windowManager = windowManager
        
        self.start_thread()

    def on_press(self,key):
        if key == keyboard.Key.alt:
            self.alt_pressed = True
        
        try :
            if self.alt_pressed and key.char == 'q':
                self.windowManager.next() 
            if self.alt_pressed and key.char == 's':
                self.windowManager.previous()
        except AttributeError:

            return

    def on_release(self,key):
        
        if key == keyboard.Key.alt:
            self.alt_pressed = False

    def start_thread(self):

        thread = threading.Thread(target=self.run, args=[])
        thread.daemon = True
        thread.start()

    def run(self):
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()