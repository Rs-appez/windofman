from keyboardManager import KeyboardManager
from windowConfig import WindowConfig
from windowManager import WindowManager

def main():
    
    wm = WindowManager()
    wc = WindowConfig(wm)
    KeyboardManager(wm)
    
    wm.print_windows_name()
    wc.start()



if __name__ == '__main__':
    main()