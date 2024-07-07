from machine import Pin, I2C  # type: ignore
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import utime as time  # type: ignore
from math import *

# LCD address, width, and height
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Constants for the number of rows and columns
numRows = 8  # Number of rows
numCols = 5  # Number of columns

# Define the pins for rows and columns
rowPins = [13, 12, 14, 26, 25, 5, 17, 15]
colPins = [23, 16, 4, 19, 18]

# Backlight toggle
on = -1

exit = -1

menu = {
    "Home": {
        "Calculate": None,
        "Equation Solver": {
            "Multi-variable": None,
            "Single-variable": None
        },
        "Unit Conversion": {
            "Length": "Km to m",
            "Area": None,
            "Mass": None,
            "Pressure": None,
            "Energy": None,
            "Power": None
        },
        "Saved Data": {
            "Predefined": None,
            "User Defined": None
        },
        "Settings": {
            "User Account": None,
            "Angle": None,
            "Sync": None,
            "Wifi": None,
            "Bluetooth": None
        }
    }
}

# Position
menu_nav = ["Home"]
menu_list = []
menu_pos = 0
cursor_pos = 0

def update_display():
    global menu, menu_nav, menu_list, menu_pos, cursor_pos
    current_state = menu
    for i in menu_nav:
        current_state = current_state[i]
    menu_list = list(current_state.keys())
    lcd.clear()
    for i in range(I2C_NUM_ROWS):
        line_index = cursor_pos + i
        if line_index < len(menu_list):
            lcd.move_to(0, i)
            lcd.putstr(menu_list[line_index])
    lcd.move_to(0, menu_pos - cursor_pos)

def navigate(dir):
    global menu, menu_nav, menu_list, menu_pos, cursor_pos, exit
    if dir == "d":
        if menu_pos + 1 < len(menu_list):
            menu_pos += 1
            if menu_pos >= cursor_pos + I2C_NUM_ROWS:
                cursor_pos += 1
        else:
            menu_pos = 0
            cursor_pos = 0
        update_display()
    elif dir == "u":
        if menu_pos > 0:
            menu_pos -= 1
            if menu_pos < cursor_pos:
                cursor_pos -= 1
        else:
            menu_pos = len(menu_list) - 1
            cursor_pos = max(0, menu_pos - I2C_NUM_ROWS + 1)
        update_display()
    elif dir == "r":
        menu_nav.append(menu_list[menu_pos])
        menu_pos = 0
        cursor_pos = 0
        update_display()
    elif dir == "l":
        if len(menu_nav) > 1:
            menu_nav.pop()
        else:
            exit*=-1
            # loop()
        menu_pos = 0
        cursor_pos = 0
        update_display()
    return 0

def home():
    global menu, menu_nav, menu_list, menu_pos, cursor_pos
    menu_nav = ["Home"]
    menu_list = []
    menu_pos = 0
    cursor_pos = 0
    update_display()
    return 0

def default_key(r, c):
    if r == 0:
        if c == 2:
            navigate("u")
        elif c == 3:
            home()
    elif r == 1:
        if c == 1:
            navigate("l")
        elif c == 2:
            navigate("r")
        elif c == 3:
            navigate("r")
    elif r == 2:
        if c == 2:
            navigate("d")
    return 0

def setup():
    global exit
    exit=-1
    print("Setup")
    lcd.backlight_off()
    lcd.show_cursor()
    lcd.clear()
    
    # Set row pins as INPUT_PULLUP
    for pin in rowPins:
        Pin(pin, Pin.IN, Pin.PULL_UP)
    
    # Set column pins as OUTPUT and HIGH
    for pin in colPins:
        p = Pin(pin, Pin.OUT)
        p.value(1)

def loop():
    while exit<0:
        # Loop through each column
        for col in range(numCols):
            # Activate the current column
            Pin(colPins[col], Pin.OUT).value(0)
            
            # Check each row in the current column
            for row in range(numRows):
                buttonState = Pin(rowPins[row], Pin.IN, Pin.PULL_UP).value()
                
                # If button is pressed (LOW), print the row and column
                if buttonState == 0:
                    # if row==0 and col==3:
                    #     return 0
                    default_key(row, col)
                    time.sleep(0.2)  # Debounce delay
            
            # Deactivate the current column
            Pin(colPins[col], Pin.OUT).value(1)


def menu_fun():
    setup()
    # home()
    loop()
