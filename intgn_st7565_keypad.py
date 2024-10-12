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
    " ": [0b00000000],  # Space
    "1": [0b00100010, 0b00111110, 0b00100000],
    "2": [0b00110010, 0b00101010, 0b00101110],
    "3": [0b00100010, 0b00101010, 0b00111110],
    "4": [0b00001110, 0b00001000, 0b00111110],
    "5": [0b00101110, 0b00101010, 0b00111010],
    "6": [0b00111110, 0b00101010, 0b00111010],
    "7": [0b00000010, 0b00000010, 0b00111110],
    "8": [0b00111110, 0b00101010, 0b00111110],
    "9": [0b00101110, 0b00101010, 0b00111110],
    "0": [0b00111110, 0b00100010, 0b00111110],

    "A": [0b00111110, 0b00010010, 0b00111110],  # Letter A
    "B": [0b00111110, 0b00101010, 0b00110110],  # Letter B
    "C": [0b00111110, 0b00100010, 0b00100010],  # Letter C
    "D": [0b00111110, 0b00100010, 0b00111110],  # Letter D
    "E": [0b00111110, 0b00101010, 0b00101010],  # Letter E
    "F": [0b00111110, 0b00001010, 0b00001010],  # Letter F
    "G": [0b00111110, 0b00101010, 0b00111010],  # Letter G
    "H": [0b00111110, 0b00001000, 0b00111110],  # Letter H
    "I": [0b00100010, 0b00111110, 0b00100010],  # Letter I
    "J": [0b00110000, 0b00100000, 0b00111110],  # Letter J
    "K": [0b00111110, 0b00001000, 0b00110110],  # Letter K
    "L": [0b00111110, 0b00100000, 0b00100000],  # Letter L
    "M": [0b00111110, 0b00000100, 0b00111110],  # Letter M
    "N": [0b00111110, 0b00011000, 0b00111110],  # Letter N
    "O": [0b00111110, 0b00100010, 0b00111110],  # Letter O
    "P": [0b00111110, 0b00001010, 0b00001110],  # Letter P
    "Q": [0b00111110, 0b00110010, 0b00111110],  # Letter Q
    "R": [0b00111110, 0b00011010, 0b00101110],  # Letter R
    "S": [0b00101110, 0b00101010, 0b00111010],  # Letter S
    "T": [0b00000010, 0b00111110, 0b00000010],  # Letter T
    "U": [0b00111110, 0b00100000, 0b00111110],  # Letter U
    "V": [0b00111110, 0b00010000, 0b00111110],  # Letter V
    "W": [0b00111110, 0b00010000, 0b00111110],  # Letter W
    "X": [0b00110110, 0b00001000, 0b00110110],  # Letter X
    "Y": [0b00001110, 0b00110000, 0b00001110],  # Letter Y
    "Z": [0b00110010, 0b00101010, 0b00100110],  # Letter Z

    "-": [0b00001000, 0b00001000, 0b00001000],  # Dash
    "_": [0b00100000, 0b00100000, 0b00100000],  # Underscore
    "=": [0b00001010, 0b00001010, 0b00001010],  # Equals sign
    "+": [0b00001000, 0b00011100, 0b00001000],  # Plus sign
    ".": [0b00100000],                          # Period
    ",": [0b00100000, 0b00010000],              # Comma
    ":": [0b00100100],                          # Colon
    ";": [0b00100000, 0b00010100],              # Semicolon
    "!": [0b00111110],                          # Exclamation mark
    "?": [0b00000010, 0b00101010, 0b00001110],  # Question mark
}

init_display()

# Clear the display
clear_display()
for pin in colPins:
    Pin(pin, Pin.IN, Pin.PULL_UP)

# Set column pins as OUTPUT and HIGH
for pin in rowPins:
    p = Pin(pin, Pin.OUT)
    p.value(1)
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
                    # default_key(row, col)
                    print("row= ",row, " ", "col= ",col)
                    str_pnt="R"+str(row)+"C"+str(col)
                    set_page_address(0)
                    set_column_address(0)
                    for i in str_pnt:
                        write_data(0b00000000)
                        for j in graph_letters[i]:
                            
                            write_data(j)
                            
                    
                    time.sleep(0.2)  # Debounce delay
                    # write_data(0b00000000)
            
            # Deactivate the current column
            
            Pin(rowPins[row], Pin.OUT).value(1)



loop()
