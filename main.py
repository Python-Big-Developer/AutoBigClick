# --- Imports ---
import multiprocessing
import pyautogui
import time
from pynput import keyboard
from colorama import Fore, init
import os
import sys

init()

# --- Variables ---
version = 1.0
click_key = 'lmb'
space = 0.1
stop_key = 'x'  # Changed to lowercase for consistency

# --- Config ---
def SetClickKey(NKey: str):
    global click_key
    if NKey in ['lmb', 'rmb']:
        click_key = NKey
        print(Fore.GREEN + f"Click key set to: {click_key}")
    else:
        if not len(list(click_key)) > 1:
            click_key = NKey
            print(Fore.GREEN + f"Click key set to: {click_key}")

def SetSpace(ntime: float):
    global space
    space = ntime
    print(Fore.GREEN + f"Space between clicks set to: {space}")

def SetStopKey(NKey):
    global stop_key
    if len(NKey) == 1:
        stop_key = NKey
        print(Fore.GREEN + f"Stop key set to: {stop_key}")

# --- Start/Stop ---
def on_press(key, ss):
    try:
        if key.char == stop_key:
            ss.value = not ss.value  # Toggle the state
            print("Clicking status:", ss.value)  # Print status
    except AttributeError:
        pass  # Ignore special keys

# --- Main ---
def AutoClicks(ss):
    global click_key, space
    while True:
        if ss.value:
            time.sleep(3)
            klikanie = True
            while klikanie:
                if ss.value:  # Check the shared variable
                    if click_key == 'lmb':
                        pyautogui.click()
                    elif click_key == 'rmb':
                        pyautogui.rightClick()
                    time.sleep(space)  # Sleep to control the click speed
                else:
                    klikanie = False

# --- InterFace ---
def napis():
    print(Fore.GREEN + '''
     _              _             ____    _            ____   _   _          _    
    / \\     _   _  | |_    ___   | __ )  (_)   __ _   / ___| | | (_)   ___  | | __          -------------------------------------
   / _ \\   | | | | | __|  / _ \\  |  _ \\  | |  / _` | | |     | | | |  / __| | |/ /          Made by Lunachar
  / ___ \\  | |_| | | |_  | (_) | | |_) | | | | (_| | | |___  | | | | | (__  |   <           Thank's :) Type /help to command list
 /_/   \\_\\  \\__,_|  \\__|  \\___/  |____/  |_|  \\__, |  \\____| |_| |_|  \\___| |_|\\_|          -------------------------------------
                                              |___/                               
''')

# --- Run ---
if __name__ == "__main__":
    # Create a shared boolean variable
    ss = multiprocessing.Value('b', False)

    # Set up the keyboard listener
    listener = keyboard.Listener(on_press=lambda key: on_press(key, ss))
    listener.start()

    # Start the AutoClicks process
    AC = multiprocessing.Process(target=AutoClicks, args=(ss,))
    AC.start()

    # Print the interface
    napis()
    while True:
        command = input('C/: ')
        if command == '/help':
            print(f''' Command list:
                Buttons:
Press {stop_key} to start/stop AutoClicker
            Commands:
/help – List of commands
/setkey – To set the pressed button
/setspace – To set a pause between clicks
/clear - To clear console
/exit - To exit the program
/info - Informations of the program
''')
        elif command == '/setkey':
            nkey = input('Enter a new click key (lmb/rmb): ')
            SetClickKey(nkey)
        elif command == '/clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            napis()
        elif command == '/setspace':
            try:
                nspace = float(input('Enter a new space value (in seconds): '))
                SetSpace(nspace)
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter a numeric value.")
        elif command == '/exit':
            print(Fore.YELLOW + "Exiting the program...")
            ss.value = False  # Stop the clicking process
            AC.terminate()  # Terminate the AutoClicks process
            AC.join()  # Wait for the process to finish
            listener.stop()  # Stop the keyboard listener
            sys.exit()  # Exit the program
        elif command == '/info':
            print(Fore.CYAN + f'''
----------------------------------------------------------
|    AutoBigClick v{version}                                   |    
|    Made by Lunachar                                    |
|    GitHub: https://github.com/Python-Big-Developer/    |
----------------------------------------------------------
                  ''' + Fore.GREEN)
        else:
            print('')
            print(Fore.RED + 'The command is not registered')
            print(Fore.GREEN)
