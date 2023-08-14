from keyboardManager import KeyboardManager
from windowManager import WindowManager

def main():
    
    wm = WindowManager()
    KeyboardManager(wm)

    wm.print_windows_name()

    while 1 :
        pass



if __name__ == '__main__':
    main()