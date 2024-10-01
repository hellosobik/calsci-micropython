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
    write_instruction(0x16)  # Contrast level (set to 0x16 here)
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

def plot_function(fb, func, x_min, x_max, y_min, y_max, width, height):
    global x_past, y_past
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

        # Ensure y_pixel is within the display range
        if 0 <= y_pixel < height:
            
            fb.pixel(x_pixel-1, y_pixel-1, 1)
            # if x_past!=0 and y_past!=0:
            if x_past*y_past!=0:
                fb.line(x_past, y_past, x_pixel-1, y_pixel-1, 1)
            x_past=x_pixel-1
            y_past=y_pixel-1

def polynom(x):
    y=e**(2-0.2*x)
    return y

fb.line(0,31,127,31, 1)
fb.line(63,0,63,63,1)

resolution=7
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
