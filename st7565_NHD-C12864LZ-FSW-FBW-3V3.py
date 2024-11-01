import machine
import time
import framebuf
from math import *
# Pin definitions for ESP32
CS1 = machine.Pin(5, machine.Pin.OUT)  # Chip Select
RS = machine.Pin(19, machine.Pin.OUT)  # Register Select (A0 on ST7565R)
RST = machine.Pin(17, machine.Pin.OUT) # Reset
SDA = machine.Pin(23, machine.Pin.OUT) # MOSI (Data)
SCK = machine.Pin(18, machine.Pin.OUT) # SCLK (Clock)

# SPI Configuration for the display (SPI communication)
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0, sck=SCK, mosi=SDA)

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


# Create a buffer for the display (128x64, monochrome: 1 bit per pixel)
buffer = bytearray((128*64)//8)  # 128x64 pixels, 1 bit per pixel
fb = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_VLSB)

def bytearray_to_binary_visual_list(byte_arr):
    # Convert each byte in the bytearray to a binary string with 8 bits, keeping the '0b' prefix
    binary_list = []
    for byte in byte_arr:
        # Use bitwise operations to manually convert to 8-bit binary string
        binary_string = '0b' + ''.join('1' if byte & (1 << (7 - bit)) else '0' for bit in range(8))
        binary_list.append(binary_string)
    return binary_list

# Example usage
byte_arr = bytearray([0x3F, 0xA5, 0xFF, 0x00])  # Example bytearray
binary_visual_list = bytearray_to_binary_visual_list(buffer)

# Initialize the display
init_display()

# Clear the display
clear_display()

x_past=0
y_past=0

# graph_letters={
#     " ":[0b00000000],
#     "1":[0b00100010,0b00111110,0b00100000],
#     "2":[0b00110010,0b00101010,0b00101110],
#     "3":[0b00100010,0b00101010,0b00111110]
# }

graph_letters = {
    " ": [0b00000000],  # Space
    "1": [0b00100010, 0b00111110, 0b00100000],
    "2": [0b00110010, 0b00101010, 0b00101110],
    "3": [0b00100010, 0b00101010, 0b00111110],
    "4": [0b00001110, 0b00001000, 0b00111110],
    "5": [0b00101110, 0b00101010, 0b00111010],
    "6": [0b00111110, 0b00101010, 0b00111010],
    "7": [0b00000010, 0b00111110, 0b00000010],
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


def plot_function(fb, func, x_min, x_max, y_min, y_max, width, height):
    global x_past, y_past, graph_letters
    # Scale factors to map function values to the display's pixel coordinates
    x_scale = (x_max - x_min) /(width)
    y_scale = (y_max - y_min) / (height)

    # Loop through each x pixel
    for x_pixel in range(width):
        
        # Convert the pixel x-coordinate to the mathematical x-value
        x_value = x_min + (x_pixel) * x_scale

        # Calculate the corresponding y-value for the function
        y_value = func(x_value)

        # Scale the y-value to the display height and invert it (because displays usually have y=0 at the top)
        y_pixel = int(height - (y_value - y_min) / y_scale)
        
        if func(x_value)>y_max or func(x_value)<y_min:

            print(" pixel= ",x_pixel," ", y_pixel," value= ",x_value," ", y_value ," past= ",x_past," ",y_past)
            x_past=0
            y_past=0
            # fb.vline(x_pixel,y_pixel, 100,1)

        # Ensure y_pixel is within the display range
        if 0 <= y_pixel < height:
            
            fb.pixel(x_pixel-1, y_pixel-1, 1)
            # if x_past!=0 and y_past!=0:
            if x_past*y_past!=0:
                fb.line(x_past, y_past, x_pixel-1, y_pixel-1, 1)
            x_past=x_pixel-1
            y_past=y_pixel-1
    #numbering
    fb.line(31,33,31,29,1)
    fb.line(95,33,95,29,1)
    fb.hline(62,0,4,1)
    fb.hline(62,63,4,1)


def polynom(x):
    # y=sin(x)
    # y=x*sin(x)
    # y=e**x
    # y=0
    # if x in range[-1,1]:
    #     y=asin(x)
    # y=tan(x)
    # if x<0:
    #     y=-1
    # if x>0:
    #     y=1
    if x == 0:
        y=25
    else:
        y=sin(x)/x  
    return y

# def polynom2(x):
#     # y=sin(x)
#     y=sin(x)
#     return y

fb.line(0,31,127,31, 1)
fb.line(63,0,63,63,1)

# fb.text("3", 31, 31, 1)

resolution=4
x_res=2
y_res=1

plot_function(fb, polynom, -resolution*x_res, resolution*x_res, -resolution*y_res, resolution*y_res, 128, 64)

print("")
print("")
binary_visual_list = bytearray_to_binary_visual_list(buffer)


def update_display():
    for page in range(8):  # ST7565R has 8 pages (for 64 pixels in height, each page is 8 pixels)
        set_page_address(page)
        set_column_address(0)
        for i in range(128):  # Send all 128 columns of the current page
            write_data(eval(binary_visual_list[page * 128 + i]))


# # Example: after drawing, call update_display() to refresh the display with the current buffer
update_display()

set_page_address(4)
set_column_address(26)
for i in graph_letters["-"]:
    write_data(i)
# for i in graph_letters["2"]:
#     write_data(i)
for i in graph_letters[" "]:
    write_data(i)
for i in graph_letters["R"]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)

set_page_address(4)
set_column_address(26+64)
for i in graph_letters["+"]:
    write_data(i)
# for i in graph_letters["2"]:
#     write_data(i)
for i in graph_letters[" "]:
    write_data(i)
for i in graph_letters["R"]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)

set_page_address(0)
set_column_address(55)
for i in graph_letters["+"]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)
for i in graph_letters["R"]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)

set_page_address(7)
set_column_address(55)
for i in graph_letters["-"]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)
for i in graph_letters["R"]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)

set_page_address(7)
set_column_address(112)
for i in graph_letters["R"]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)
for i in graph_letters["="]:
    write_data(i)
for i in graph_letters[" "]:
    write_data(i)
for i in graph_letters[str(resolution)]:
    write_data(i)

