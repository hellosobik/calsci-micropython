from machine import Pin, I2C, SPI  # type: ignore
import utime as time  # type: ignore


# # Constants for the number of rows and columns
numRows = 8  # Number of rows
numCols = 5  # Number of columns


CS1 = Pin(2, Pin.OUT)  # Chip Select
RS = Pin(32, Pin.OUT)  # Register Select (A0 on ST7565R)
RST = Pin(33, Pin.OUT) # Reset
SDA = Pin(27, Pin.OUT) # MOSI (Data)
SCK = Pin(26, Pin.OUT) # SCLK (Clock)

rowPins = [4, 5, 13, 14, 15, 16, 17, 18]
colPins = [19, 21, 22, 23, 25]

# SPI Configuration for the display (SPI communication)
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=SCK, mosi=SDA)

# Helper functions
def write_instruction(cmd):
    RS.value(0)  # Set RS to 0 for command
    CS1.value(0)  # Activate chip select
    spi.write(bytearray([cmd]))  # Write command via SPI
    CS1.value(1)  # Deactivate chip select

def write_data(data):
    RS.value(1)  # Set RS to 1 for data
    CS1.value(0)  # Activate chip select
    spi.write(bytearray([data]))  # Write data via SPI
    CS1.value(1)  # Deactivate chip select

def delay(ms):
    time.sleep_ms(ms)

# Initialization sequence (based on ST7565R datasheet)
def init_display():
    RST.value(0)  # Reset the display
    delay(50)
    RST.value(1)  # End reset

    write_instruction(0xAE)  # Display OFF
    write_instruction(0xA2)  # Set Bias 1/9 (default)
    write_instruction(0xA0)  # Set ADC normal
    write_instruction(0xC8)  # Set COM output direction, normal mode
    write_instruction(0xA6)  # Display normal (not inverted)
    write_instruction(0x2F)  # Power control: Booster, Regulator, Follower on
    write_instruction(0x27)  # Set contrast (0x27 can be adjusted)
    write_instruction(0x81)  # Set contrast
    write_instruction(0x0A)  # Contrast level (set to 0x16 here)
    write_instruction(0xAF)  # Display ON

# Pixel setting functions
def set_page_address(page):
    write_instruction(0xB0 | page)  # Set page address (B0h to B7h)

def set_column_address(column):
    write_instruction(0x10 | (column >> 4))  # Set higher column address
    write_instruction(0x00 | (column & 0x0F))  # Set lower column address


# Clear the entire display
def clear_display():
    for page in range(8):  # Assuming an 8-page display
        set_page_address(page)
        set_column_address(0)
        for column in range(128):  # Assuming 128 columns
            write_data(0x00)  # Clear all columns


graph_letters = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],  # Space
    '!': [0x00, 0x00, 0x5F, 0x00, 0x00, 0x00, 0x00, 0x00],  # !
    '"': [0x00, 0x07, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00],  # "
    '#': [0x14, 0x7F, 0x14, 0x7F, 0x14, 0x00, 0x00, 0x00],  # #
    '$': [0x24, 0x2A, 0x7F, 0x2A, 0x12, 0x00, 0x00, 0x00],  # $
    '%': [0x23, 0x13, 0x08, 0x64, 0x62, 0x00, 0x00, 0x00],  # %
    '&': [0x36, 0x49, 0x55, 0x22, 0x50, 0x00, 0x00, 0x00],  # &
    "'": [0x00, 0x05, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00],  # '
    '(': [0x00, 0x1C, 0x22, 0x41, 0x00, 0x00, 0x00, 0x00],  # (
    ')': [0x00, 0x41, 0x22, 0x1C, 0x00, 0x00, 0x00, 0x00],  # )
    '*': [0x14, 0x08, 0x3E, 0x08, 0x14, 0x00, 0x00, 0x00],  # *
    '+': [0x08, 0x08, 0x3E, 0x08, 0x08, 0x00, 0x00, 0x00],  # +
    ',': [0x00, 0x50, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00],  # ,
    '-': [0x08, 0x08, 0x08, 0x08, 0x08, 0x00, 0x00, 0x00],  # -
    '.': [0x00, 0x60, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00],  # .
    '/': [0x20, 0x10, 0x08, 0x04, 0x02, 0x00, 0x00, 0x00],  # /
    '0': [0x3E, 0x51, 0x49, 0x45, 0x3E, 0x00, 0x00, 0x00],  # 0
    '1': [0x00, 0x42, 0x7F, 0x40, 0x00, 0x00, 0x00, 0x00],  # 1
    '2': [0x42, 0x61, 0x51, 0x49, 0x46, 0x00, 0x00, 0x00],  # 2
    '3': [0x21, 0x41, 0x45, 0x4B, 0x31, 0x00, 0x00, 0x00],  # 3
    '4': [0x18, 0x14, 0x12, 0x7F, 0x10, 0x00, 0x00, 0x00],  # 4
    '5': [0x27, 0x45, 0x45, 0x45, 0x39, 0x00, 0x00, 0x00],  # 5
    '6': [0x3C, 0x4A, 0x49, 0x49, 0x30, 0x00, 0x00, 0x00],  # 6
    '7': [0x01, 0x71, 0x09, 0x05, 0x03, 0x00, 0x00, 0x00],  # 7
    '8': [0x36, 0x49, 0x49, 0x49, 0x36, 0x00, 0x00, 0x00],  # 8
    '9': [0x06, 0x49, 0x49, 0x29, 0x1E, 0x00, 0x00, 0x00],  # 9
    ':': [0x00, 0x36, 0x36, 0x00, 0x00, 0x00, 0x00, 0x00],  # :
    ';': [0x00, 0x56, 0x36, 0x00, 0x00, 0x00, 0x00, 0x00],  # ;
    '<': [0x08, 0x14, 0x22, 0x41, 0x00, 0x00, 0x00, 0x00],  # <
    '=': [0x14, 0x14, 0x14, 0x14, 0x14, 0x00, 0x00, 0x00],  # =
    '>': [0x41, 0x22, 0x14, 0x08, 0x00, 0x00, 0x00, 0x00],  # >
    '?': [0x02, 0x01, 0x51, 0x09, 0x06, 0x00, 0x00, 0x00],  # ?
    '@': [0x32, 0x49, 0x79, 0x41, 0x3E, 0x00, 0x00, 0x00],  # @
    'A': [0x7E, 0x11, 0x11, 0x11, 0x7E, 0x00, 0x00, 0x00],  # A
    'B': [0x7F, 0x49, 0x49, 0x49, 0x36, 0x00, 0x00, 0x00],  # B
    'C': [0x3E, 0x41, 0x41, 0x41, 0x22, 0x00, 0x00, 0x00],  # C
    'D': [0x7F, 0x41, 0x41, 0x22, 0x1C, 0x00, 0x00, 0x00],  # D
    'E': [0x7F, 0x49, 0x49, 0x49, 0x41, 0x00, 0x00, 0x00],  # E
    'F': [0x7F, 0x09, 0x09, 0x09, 0x01, 0x00, 0x00, 0x00],  # F
    'G': [0x3E, 0x41, 0x49, 0x49, 0x7A, 0x00, 0x00, 0x00],  # G
    'H': [0x7F, 0x08, 0x08, 0x08, 0x7F, 0x00, 0x00, 0x00],  # H
    'I': [0x00, 0x41, 0x7F, 0x41, 0x00, 0x00, 0x00, 0x00],  # I
    'J': [0x20, 0x40, 0x41, 0x3F, 0x01, 0x00, 0x00, 0x00],  # J
    'K': [0x7F, 0x08, 0x14, 0x22, 0x41, 0x00, 0x00, 0x00],  # K
    'L': [0x7F, 0x40, 0x40, 0x40, 0x40, 0x00, 0x00, 0x00],  # L
    'M': [0x7F, 0x02, 0x0C, 0x02, 0x7F, 0x00, 0x00, 0x00],  # M
    'N': [0x7F, 0x04, 0x08, 0x10, 0x7F, 0x00, 0x00, 0x00],  # N
    'O': [0x3E, 0x41, 0x41, 0x41, 0x3E, 0x00, 0x00, 0x00],  # O
    'P': [0x7F, 0x09, 0x09, 0x09, 0x06, 0x00, 0x00, 0x00],  # P
    'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E, 0x00, 0x00, 0x00],  # Q
    'R': [0x7F, 0x09, 0x19, 0x29, 0x46, 0x00, 0x00, 0x00],  # R
    'S': [0x46, 0x49, 0x49, 0x49, 0x31, 0x00, 0x00, 0x00],  # S
    'T': [0x01, 0x01, 0x7F, 0x01, 0x01, 0x00, 0x00, 0x00],  # T
    'U': [0x3F, 0x40, 0x40, 0x40, 0x3F, 0x00, 0x00, 0x00],  # U
    'V': [0x1F, 0x20, 0x40, 0x20, 0x1F, 0x00, 0x00, 0x00],  # V
    'W': [0x3F, 0x40, 0x38, 0x40, 0x3F, 0x00, 0x00, 0x00],  # W
    'X': [0x63, 0x14, 0x08, 0x14, 0x63, 0x00, 0x00, 0x00],  # X
    'Y': [0x07, 0x08, 0x70, 0x08, 0x07, 0x00, 0x00, 0x00],  # Y
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43, 0x00, 0x00, 0x00],  # Z
    '[': [0x00, 0x7F, 0x41, 0x41, 0x00, 0x00, 0x00, 0x00],  # [
    '\\': [0x02, 0x04, 0x08, 0x10, 0x20, 0x00, 0x00, 0x00], # \
    ']': [0x00, 0x41, 0x41, 0x7F, 0x00, 0x00, 0x00, 0x00],  # ]
    '^': [0x04, 0x02, 0x01, 0x02, 0x04, 0x00, 0x00, 0x00],  # ^
    '_': [0x40, 0x40, 0x40, 0x40, 0x40, 0x00, 0x00, 0x00],  # _
    '`': [0x00, 0x03, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00],  # `
    'a': [0x20, 0x54, 0x54, 0x54, 0x78, 0x00, 0x00, 0x00],  # a
    'b': [0x7F, 0x48, 0x44, 0x44, 0x38, 0x00, 0x00, 0x00],  # b
    'c': [0x38, 0x44, 0x44, 0x44, 0x20, 0x00, 0x00, 0x00],  # c
    'd': [0x38, 0x44, 0x44, 0x48, 0x7F, 0x00, 0x00, 0x00],  # d
    'e': [0x38, 0x54, 0x54, 0x54, 0x18, 0x00, 0x00, 0x00],  # e
    'f': [0x08, 0x7E, 0x09, 0x01, 0x02, 0x00, 0x00, 0x00],  # f
    'g': [0x08, 0x14, 0x54, 0x54, 0x3C, 0x00, 0x00, 0x00],  # g
    'h': [0x7F, 0x08, 0x04, 0x04, 0x78, 0x00, 0x00, 0x00],  # h
    'i': [0x00, 0x44, 0x7D, 0x40, 0x00, 0x00, 0x00, 0x00],  # i
    'j': [0x20, 0x40, 0x44, 0x3D, 0x00, 0x00, 0x00, 0x00],  # j
    'k': [0x7F, 0x10, 0x28, 0x44, 0x00, 0x00, 0x00, 0x00],  # k
    'l': [0x00, 0x41, 0x7F, 0x40, 0x00, 0x00, 0x00, 0x00],  # l
    'm': [0x7C, 0x04, 0x78, 0x04, 0x78, 0x00, 0x00, 0x00],  # m
    'n': [0x7C, 0x08, 0x04, 0x04, 0x78, 0x00, 0x00, 0x00],  # n
    'o': [0x38, 0x44, 0x44, 0x44, 0x38, 0x00, 0x00, 0x00],  # o
    'p': [0x7C, 0x14, 0x14, 0x14, 0x08, 0x00, 0x00, 0x00],  # p
    'q': [0x08, 0x14, 0x14, 0x18, 0x7C, 0x00, 0x00, 0x00],  # q
    'r': [0x7C, 0x08, 0x04, 0x04, 0x08, 0x00, 0x00, 0x00],  # r
    's': [0x48, 0x54, 0x54, 0x54, 0x20, 0x00, 0x00, 0x00],  # s
    't': [0x04, 0x3F, 0x44, 0x40, 0x20, 0x00, 0x00, 0x00],  # t
    'u': [0x3C, 0x40, 0x40, 0x20, 0x7C, 0x00, 0x00, 0x00],  # u
    'v': [0x1C, 0x20, 0x40, 0x20, 0x1C, 0x00, 0x00, 0x00],  # v
    'w': [0x3C, 0x40, 0x30, 0x40, 0x3C, 0x00, 0x00, 0x00],  # w
    'x': [0x44, 0x28, 0x10, 0x28, 0x44, 0x00, 0x00, 0x00],  # x
    'y': [0x0C, 0x50, 0x50, 0x50, 0x3C, 0x00, 0x00, 0x00],  # y
    'z': [0x44, 0x64, 0x54, 0x4C, 0x44, 0x00, 0x00, 0x00],  # z
    '{': [0x00, 0x08, 0x36, 0x41, 0x00, 0x00, 0x00, 0x00],  # {
    '|': [0x00, 0x00, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00],  # |
    '}': [0x00, 0x41, 0x36, 0x08, 0x00, 0x00, 0x00, 0x00],  # }
    '~': [0x08, 0x08, 0x2A, 0x1C, 0x08, 0x00, 0x00, 0x00],  # ~
}

for key in graph_letters:
    # Remove the last 3 columns (last 3 elements) from each list
    graph_letters[key] = graph_letters[key][:-3]

init_display()

# Clear the display
clear_display()
for pin in colPins:
    Pin(pin, Pin.IN, Pin.PULL_UP)

# Set column pins as OUTPUT and HIGH
for pin in rowPins:
    p = Pin(pin, Pin.OUT)
    p.value(1)


def default_key(r, c):
    if r == 0:
        if c == 0:
            return ""
        elif c == 1:
            return ""
        elif c == 2:
            return "nav_u"
        elif c == 3:
            return ""
        elif c == 4:
            return ""
    elif r == 1:
        if c == 0:
            return ""
        elif c == 1:
            return "nav_l"
        elif c == 2:
            return ""
        elif c == 3:
            return "nav_r"
        elif c == 4:
            return ""
    elif r == 2:
        if c == 0:
            return ""
        elif c == 1:
            return ""
        elif c == 2:
            return "nav_d"
        elif c == 3:
            return "("
        elif c == 4:
            return ")"
    elif r == 3:
        if c == 0:
            return "pow( , "
        elif c == 1:
            return "sin("
        elif c == 2:
            return "cos("
        elif c == 3:
            return "tan("
        elif c == 4:
            return "log("
    elif r == 4:
        if c == 0:
            return "7"
        elif c == 1:
            return "8"
        elif c == 2:
            return "9"
        elif c == 3:
            return "nav_b"
        elif c == 4:
            return ""
    elif r == 5:
        if c == 0:
            return "4"
        elif c == 1:
            return "5"
        elif c == 2:
            return "6"
        elif c == 3:
            return "*"
        elif c == 4:
            return "/"
    elif r == 6:
        if c == 0:
            return "1"
        elif c == 1:
            return "2"
        elif c == 2:
            return "3"
        elif c == 3:
            return "+"
        elif c == 4:
            return "-"
    elif r == 7:
        if c == 0:
            return "."
        elif c == 1:
            return "0"
        elif c == 2:
            return "pow(10, "
        elif c == 3:
            return ""
        elif c == 4:
            return ""
    return 0


def loop():
    
    global numRows, rowPins, numCols, colPins, graph_letters
    while True:
        # Loop through each column
        # for col in range(numCols):
        for row in range(numRows):
            # Activate the current column
            # Pin(colPins[col], Pin.OUT).value(0)
            Pin(rowPins[row], Pin.OUT).value(0)
            
            
            # Check each row in the current column
            # for row in range(numRows):
            for col in range(numCols):
                # buttonState = Pin(rowPins[row], Pin.IN, Pin.PULL_UP).value()
                buttonState = Pin(colPins[col], Pin.IN, Pin.PULL_UP).value()
                
                # If button is pressed (LOW), print the row and column
                if buttonState == 0:
                    str=default_key(row, col)
                    # print("row= ",row, " ", "col= ",col)
                    # str_pnt="R"+str(row)+"C"+str(col)
                    # set_page_address(r)
                    # set_column_address(0)
                    # for i in txt:
                    #     write_data(0b00000000)
                    #     for j in graph_letters[i]:
                            
                    #         write_data(j)
                    # time.sleep(0.1) 
                    # return str
                    time.sleep(0.01)  # Debounce delay
                    Pin(rowPins[row], Pin.OUT).value(1)
                    return str
                    # write_data(0b00000000)
            
            # Deactivate the current column
            
            Pin(rowPins[row], Pin.OUT).value(1)
        # break



# loop()


# import os
# import sys

# def clear():

# Call the clear function
# clear()


# menu_buffer=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
text_buffer="Mechanical engineering designs, analyzes, and improves systems."
# text_buffer=""
# text_buffer="nagesh"
menu_buffer_size=len(text_buffer)
menu_buffer=list(range(menu_buffer_size))
# menu_buffer=["angle", "fun", "consts", "equations", "search", "cloud", "wifi", "settings"]
menu_buffer_cursor=0
rows=8
cols=20
display_buffer_position=0
display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
no_last_spaces=0
while True:
    if len(text_buffer)%cols!=0:
        no_last_spaces=cols-len(text_buffer)%cols
        for i in range(0,cols-len(text_buffer)%cols):
            text_buffer+=" "
            menu_buffer_size=len(text_buffer)
            menu_buffer=list(range(menu_buffer_size))
    while len(text_buffer)<=display_buffer[-1] or len(text_buffer)<rows*cols:
        no_last_spaces+=1
        text_buffer+=" "
        menu_buffer_size=len(text_buffer)
        menu_buffer=list(range(menu_buffer_size))
    display_buffer=menu_buffer[display_buffer_position:display_buffer_position+rows*cols]
    # os.system('clear')
    # clear()
    counter=0
    for i in range(rows):
        # print("")
        row=""
        for j in range(cols):
            if counter >= len(display_buffer):
                row+="\t"
            elif display_buffer[counter]==menu_buffer_cursor:
                row+="|"+str(text_buffer[display_buffer[counter]])
            else:
                row+=""+str(text_buffer[display_buffer[counter]])
            counter+=1
        # print(row)
        # loop(txt=row,r=i)
        set_page_address(i)
        set_column_address(0)
        for i in row:
            write_data(0b00000000)
            for j in graph_letters[i]:
                
                write_data(j)
        for k in range(8):
            write_data(0b00000000)

    # print("")
    # text=input("Enter the text: ")
    text=loop()
    if text=="nav_d" or text =="nav_r":
        if text=="nav_d":
            menu_buffer_cursor+=cols
        else:
            menu_buffer_cursor+=1
        if menu_buffer_cursor >= len(menu_buffer)-no_last_spaces:
            menu_buffer_cursor=0
            display_buffer_position=0
        elif menu_buffer_cursor > display_buffer[-1]:
            display_buffer_position+=cols
    elif text=="nav_u" or text=="nav_l":
        if text=="nav_u":
            menu_buffer_cursor-=cols
        else:
            menu_buffer_cursor-=1
        if menu_buffer_cursor < 0:
            menu_buffer_cursor=len(menu_buffer)-no_last_spaces-1
            display_buffer_position=len(menu_buffer)-rows*cols
        elif menu_buffer_cursor < display_buffer[0]:
            display_buffer_position-=cols
    elif text=="nav_b":
        if menu_buffer_cursor < 0:
            menu_buffer_cursor=0
            display_buffer_position=0
        elif menu_buffer_cursor < display_buffer[0]:
            text_buffer=text_buffer[0:menu_buffer_cursor-1]+text_buffer[menu_buffer_cursor:len(text_buffer)]
            display_buffer_position-=cols
            menu_buffer_size=len(text_buffer)
            menu_buffer_cursor-=1
        elif menu_buffer_cursor > 0 and menu_buffer_cursor>=display_buffer[0]:
            text_buffer=text_buffer[0:menu_buffer_cursor-1]+text_buffer[menu_buffer_cursor:len(text_buffer)]
            menu_buffer_size=len(text_buffer)
            menu_buffer_cursor-=1
    else:
        text_buffer=text_buffer[0:menu_buffer_cursor]+text+text_buffer[menu_buffer_cursor:len(text_buffer)]
        menu_buffer_size+=len(text)
        menu_buffer=list(range(menu_buffer_size))
        menu_buffer_cursor+=len(text)
        if menu_buffer_cursor>display_buffer[-1]:
            display_buffer_position=menu_buffer_cursor-menu_buffer_cursor%cols-((rows-1)*cols)
    text_buffer=text_buffer.strip()+" "
