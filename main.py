from keyboardManager import KeyboardManager
from windowConfig import WindowConfig
from windowManager import WindowManager

def main():
    
    wm = WindowManager()
    wc = WindowConfig()
    KeyboardManager(wm)
    

    wc.start()

    wm.print_windows_name()

    while 1 :
        pass

if __name__ == '__main__':
    main()