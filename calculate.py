from machine import Pin, I2C # type: ignore
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import utime as time # type: ignore
from math import *
from menu import menu_fun
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

big_text = "Creating a 10,000-word essay on mechanical engineering in a single paragraph is highly unconventional and impractical for readability and comprehension."

# String buffer
text = ""
# String r1=""
# String r2=""

# Position
text_pos = 0
cursor_pos = 0

def update_pos(text_nav):
    global cursor_pos, text_pos, text
    if cursor_pos < 0 and text_pos == 0:
        cursor_pos = len(text) % 32
        text_pos = (len(text) // 32) * 32
        return 0
    if text_nav == "text":
        if cursor_pos > 32:
            if cursor_pos < (32 + 16):
                text_pos += 16
                cursor_pos -= 16
            else:
                text_pos = (len(text) // 32) * 32
                cursor_pos = cursor_pos % 32
        elif cursor_pos < 0:
            text_pos -= 16
            cursor_pos += 16
    elif text_nav == "nav":
        if (cursor_pos + text_pos) > len(text):
            cursor_pos = 0
            text_pos = 0
        elif cursor_pos >= 32 or cursor_pos < 0:
            if cursor_pos >= 32:
                cursor_pos -= 16
                text_pos += 16
            else:
                cursor_pos += 16
                text_pos -= 16
    return 0

def update_display():
    lcd.clear()
    for i in range(32):
        char_index = text_pos + i
        if char_index < len(text):
            lcd.move_to(i % 16, i // 16)
            lcd.putchar(text[char_index])
    if cursor_pos >= 0:
        lcd.move_to(cursor_pos % 16, cursor_pos // 16)
    return 0

def new_text(data):
    global text, cursor_pos, text_pos
    if len(data) > 0:
        text = text[:text_pos + cursor_pos] + data + text[text_pos + cursor_pos:]
        cursor_pos += len(data)
    elif data == "" and not (cursor_pos == 0 and text_pos == 0):
        rem = text_pos + cursor_pos - 1
        text = text[:rem] + text[rem + 1:]
        cursor_pos -= 1
    update_pos("text")
    update_display()
    print(f"text_pos={text_pos} and cursor_pos={cursor_pos}")
    return 0

def navigate(dir):
    global cursor_pos
    if dir == "l":
        cursor_pos -= 1
    elif dir == "r":
        cursor_pos += 1
    elif dir == "u":
        cursor_pos -= 16
    elif dir == "d":
        cursor_pos += 16
    update_pos("nav")
    update_display()
    print(f"text_pos={text_pos} and cursor_pos={cursor_pos}")
    return 0

def backspace():
    new_text("")
    return 0

def allclear():
    global text, cursor_pos, text_pos
    text = ""
    cursor_pos = 0
    text_pos = 0
    new_text("")
    return 0

def backlight_toggle(one):
    global on
    if one > 0:
        lcd.backlight_off()
    else:
        lcd.backlight_on()
    on *= -1
    return 0

def dif(expr, num):
    y1=eval(expr.replace("x", str(num-0.0001)))
    y2=eval(expr.replace("x", str(num+0.0001)))
    result=(y2-y1)/0.0002
    print(y1, y2, result)
    return result


def sol():
    global text
    expression = text
    try:
        result = eval(expression)
        buffer = f"{result:.6f}"
        # Print the result to the LCD
        lcd.clear()
        lcd.putstr("Result:")
        lcd.move_to(0, 1)
        lcd.putstr(buffer[:15])
    except Exception as e:
        # Handle parse error
        lcd.clear()
        # lcd.putstr(e)
        print(e)
        buffer = ""
    return buffer[:15]

def answer():
    global text, cursor_pos, text_pos
    sol_text = sol()
    text = ""
    cursor_pos = 0
    text_pos = 0
    new_text(sol_text)
    return 0

def alpha():
    new_text(big_text)
    return 0

def beta():
    return 0

def home():
    menu_fun()
    navigate("l")
    navigate("r")

    return 0

def power_on():
    return 0

def ok():
    return 0

def blank():
    new_text("x")
    return 0

def diff():
    new_text("dif(\"\",)")
    return 0

def fx():
    return 0

def default_key(r, c):
    if r == 0:
        if c == 0:
            alpha()
        elif c == 1:
            beta()
        elif c == 2:
            navigate("u")
        elif c == 3:
            home()
        elif c == 4:
            power_on()
    elif r == 1:
        if c == 0:
            backlight_toggle(on)
        elif c == 1:
            navigate("l")
        elif c == 2:
            ok()
        elif c == 3:
            navigate("r")
        elif c == 4:
            blank()
    elif r == 2:
        if c == 0:
            diff()
        elif c == 1:
            fx()
        elif c == 2:
            navigate("d")
        elif c == 3:
            new_text("(")
        elif c == 4:
            new_text(")")
    elif r == 3:
        if c == 0:
            new_text("pow( , ")
        elif c == 1:
            new_text("sin(")
        elif c == 2:
            new_text("cos(")
        elif c == 3:
            new_text("tan(")
        elif c == 4:
            new_text("log(")
    elif r == 4:
        if c == 0:
            new_text("7")
        elif c == 1:
            new_text("8")
        elif c == 2:
            new_text("9")
        elif c == 3:
            new_text("")
        elif c == 4:
            allclear()
    elif r == 5:
        if c == 0:
            new_text("4")
        elif c == 1:
            new_text("5")
        elif c == 2:
            new_text("6")
        elif c == 3:
            new_text("*")
        elif c == 4:
            new_text("/")
    elif r == 6:
        if c == 0:
            new_text("1")
        elif c == 1:
            new_text("2")
        elif c == 2:
            new_text("3")
        elif c == 3:
            new_text("+")
        elif c == 4:
            new_text("-")
    elif r == 7:
        if c == 0:
            new_text(".")
        elif c == 1:
            new_text("0")
        elif c == 2:
            new_text("pow(10, ")
        elif c == 3:
            answer()
        elif c == 4:
            sol()
    return 0

def setup():
    print("Setup")
    # lcd.init()  # initialize the lcd
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
    global loop_val
    while True:
        # Loop through each column
        for col in range(numCols):
            # Activate the current column
            Pin(colPins[col], Pin.OUT).value(0)
            
            # Check each row in the current column
            for row in range(numRows):
                buttonState = Pin(rowPins[row], Pin.IN, Pin.PULL_UP).value()
                
                # If button is pressed (LOW), print the row and column
                if buttonState == 0:

                    default_key(row, col)
                    time.sleep(0.2)  # Debounce delay
            
            # Deactivate the current column
            Pin(colPins[col], Pin.OUT).value(1)
def cal_fun():

    setup()
    loop()