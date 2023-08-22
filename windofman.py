#!./venv/bin/python3
from keyboardManager import KeyboardManager
from windowConfig import WindowConfig
from windowManager import WindowManager

def main():
    
    wm = WindowManager()
    wc = WindowConfig(wm)
    KeyboardManager(wm)
    
    wc.start()

if __name__ == '__main__':
    main()
