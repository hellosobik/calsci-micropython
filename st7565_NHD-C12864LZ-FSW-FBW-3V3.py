import machine
import time
import framebuf
import math
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
    # write_instruction(0xA1)  # Reverse ADC (segment/column)
    # write_instruction(0xC8)  # Reverse COM (common/row)
    # write_instruction(0xA7) #display reverse
    # CMD_SET_DISPLAY_REVERSE = const(0xA7)

# Pixel setting functions
def set_page_address(page):
    write_instruction(0xB0 | page)  # Set page address (B0h to B7h)

def set_column_address(column):
    write_instruction(0x10 | (column >> 4))  # Set higher column address
    write_instruction(0x00 | (column & 0x0F))  # Set lower column address

def read_data():
    RS.value(1)  # Set RS to 1 for data mode
    CS1.value(0)  # Activate chip select
    # Simulate reading data from SPI (returning 0x00 since MicroPython doesn't support SPI read)
    dummy_data = bytearray([0x00])  # A dummy value for now
    spi.write_readinto(dummy_data, dummy_data)
    CS1.value(1)  # Deactivate chip select
    return dummy_data[0]  # Return the dummy byte

def set_pixel(x, y, on):
    # Calculate which page the Y coordinate falls into
    page = y // 8
    pixel_bit = y % 8
    
    # Set the page and column address
    set_page_address(page)
    set_column_address(x)
    
    # Read the current byte at the page and column
    current_byte = read_data()
    
    # Modify the specific bit within the byte to set/clear the pixel
    if on:
        current_byte |= (1 << pixel_bit)  # Set the bit
    else:
        current_byte &= ~(1 << pixel_bit)  # Clear the bit
    
    # Write the modified byte back to the display
    set_page_address(page)  # Set page again (some controllers require this)
    set_column_address(x)
    write_data(current_byte)

# Clear the entire display
def clear_display():
    for page in range(8):  # Assuming an 8-page display
        set_page_address(page)
        set_column_address(0)
        for column in range(128):  # Assuming 128 columns
            write_data(0x00)  # Clear all columns

def plot_quadratic():
    clear_display()  # Start with a clear display
    
    # Set up scaling factors to fit the graph on the 128x64 display
    # We want to map -64 <= x <= 64 (for better visualization)
    x_min = -64
    x_max = 64
    scale_x = 1  # Direct scaling for x
    scale_y = 0.1  # Scaling factor for y to fit the display vertically

    # Plot points for y = x^2
    for x in range(x_min, x_max + 1):
        y = x**2 * scale_y  # Calculate y value
        
        # Adjust coordinates to fit in the 128x64 screen
        x_screen = x + 64  # Shift x to center the graph horizontally
        y_screen = 63 - int(y)  # Invert y and adjust to display's coordinates (top-left is 0,0)
        
        # Only plot if within the display range
        if 0 <= x_screen < 128 and 0 <= y_screen < 64:
            set_pixel(x_screen, y_screen, True)  # Set the pixel

    # Optional: Draw axes
    draw_axes()

def draw_axes():
    # Draw X axis (middle of the screen horizontally)
    for x in range(0, 128):
        set_pixel(x, 32, True)  # X axis at y=32
    
    # Draw Y axis (middle of the screen vertically)
    for y in range(0, 64):
        set_pixel(64, y, True)  # Y axis at x=64
def set_contrast_binary(level):
    """
    Adjust the display contrast using binary values.
    
    Parameters:
    level (int): Contrast level (0b00000000 to 0b00111111). Higher values increase contrast.
    """
    if level < 0b00000000 or level > 0b00111111:
        raise ValueError("Contrast level must be between 0b00000000 and 0b00111111")
    
    # Send the contrast setting command in binary
    write_instruction(0b10000001)  # 0x81 in binary to start contrast setting
    
    # Send the contrast level as the second instruction (binary)
    write_instruction(level)
# Create a buffer for the display (128x64, monochrome: 1 bit per pixel)
buffer = bytearray((128*64)//8)  # 128x64 pixels, 1 bit per pixel
fb = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_VLSB)
# print(str(list(buffer)))
# def hex_to_binary_byte(hex_value):
#     # Convert hex value to an integer, then format it as an 8-bit binary string
#     return format(hex_value, '08b')

# # Example usage
# for i in buffer.:
#     hex_value = i  # Hexadecimal value
#     binary_byte = hex_to_binary_byte(hex_value)
#     print(binary_byte)  # Output: '00111111'

# def bytearray_to_binary_visual_list(byte_arr):
#     # Convert each byte in the bytearray to a binary number with '0b' prefix
#     return [bin(byte) for byte in byte_arr]

# # Example usage
# # byte_arr = bytearray([0x3F, 0xA5, 0xFF, 0x00])  # Example bytearray
# binary_visual_list = bytearray_to_binary_visual_list(buffer)
# print(binary_visual_list)  # Output: ['0b111111', '0b10100101', '0b11111111', '0b0']

# def bytearray_to_binary_visual_list(byte_arr):
#     # Convert each byte in the bytearray to a binary string with 8 bits, keeping the '0b' prefix
#     return list[0b + format(byte, 08b) for byte in byte_arr]

# # Example usage
# # byte_arr = bytearray([0x3F, 0xA5, 0xFF, 0x00])  # Example bytearray
# binary_visual_list = bytearray_to_binary_visual_list(buffer)
# print(binary_visual_list)  # Output: ['0b00111111', '0b10100101', '0b11111111', '0b00000000']

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
# print(binary_visual_list)  # Expected output: ['0b00111111', '0b10100101', '0b11111111', '0b00000000']


# import math

# def plot_function(user_function):
#     clear_display()  # Start with a clear display
    
#     # Set up scaling factors to fit the graph on the 128x64 display
#     # We want to map -64 <= x <= 64 (for better visualization)
#     x_min = -64
#     x_max = 64
#     scale_x = 1  # Direct scaling for x
#     scale_y = 0.1  # Scaling factor for y to fit the display vertically

#     # Iterate over the x values within the range
#     for x in range(x_min, x_max + 1):
#         try:
#             # Evaluate the user-defined function
#             y = eval(user_function) * scale_y  # Calculate y value

#             # Adjust coordinates to fit in the 128x64 screen
#             x_screen = x + 64  # Shift x to center the graph horizontally
#             y_screen = 63 - int(y)  # Invert y and adjust to display's coordinates (top-left is 0,0)

#             # Only plot if within the display range
#             if 0 <= x_screen < 128 and 0 <= y_screen < 64:
#                 set_pixel(x_screen, y_screen, True)  # Set the pixel
#         except:
#             # In case there's an error in the user function, skip this point
#             continue

#     # Optional: Draw axes
#     draw_axes()

# def draw_axes():
#     # Draw X axis (middle of the screen horizontally)
#     for x in range(0, 128):
#         set_pixel(x, 32, True)  # X axis at y=32
    
#     # Draw Y axis (middle of the screen vertically)
#     for y in range(0, 64):
#         set_pixel(64, y, True)  # Y axis at x=64

# Example usage:
# You can prompt the user to input their function in a real scenario


# Initialize the display
init_display()

# Clear the display
clear_display()

# Test - Set a few pixels on and off
# set_pixel(10, 10, True)  # Set pixel at (10, 10) to on
# set_pixel(20, 15, True)  # Set pixel at (20, 15) to on
# set_pixel(30, 30, True)  # Set pixel at (30, 30) to on
# set_pixel(10, 10, False) # Clear pixel at (10, 10)
# for i in range(0,50):
#     set_pixel(i,i, True)
# for i in range(0,64):
#     set_pixel(0,i, True)
#     delay(50)
# for i in range(0,50):
#     for j in range(0,50):
#         set_pixel(i,j,True)
# for i in range(0,10):
#     set_page_address(2)
#     set_column_address(10+i)
#     write_data(0xFF)
# for i in range(0,8):
#     for j in range(0,8):
#         set_page_address(i)
#         set_column_address(i*8+j)
#         write_data(0xFF)
# write_instruction(0b10100111)
# set_contrast_binary(0b00000000)

# write_instruction(0b10100101)
# plot_quadratic()
# for k in range(0,3):
#     for i in range(k+2,8):
#         for j in range(0,8):
#             set_page_address(i)
#             set_column_address(i*8+j+16*k)
#             write_data(0xFF)


# for j in range(0,8):
#     set_page_address(2)
#     set_column_address(j)
#     write_data(0xFF)

# user_function = input("Enter a function of x (e.g., 'x**2 - 2*x + 1'): ")
# plot_function(user_function)
# write_instruction(0b10100101)
# write_instruction(0b10110000)
# write_instruction(0b00010000)
# write_instruction(0b00000000)
# write_instruction(0b10110000)
# write_data(0b00000001)
# Clear the buffer (fill the screen with black)
def plot_function(fb, func, x_min, x_max, y_min, y_max, width, height):
    """
    Plots the graph of a function on the framebuffer.
    
    Parameters:
    - fb: The frame buffer object
    - func: The mathematical function to plot (should accept an x-value and return a y-value)
    - x_min, x_max: The range of x-values to plot
    - y_min, y_max: The range of y-values to plot
    - width: The width of the display in pixels
    - height: The height of the display in pixels
    """
    # Scale factors to map function values to the display's pixel coordinates
    x_scale = (x_max - x_min) /(width/3)
    y_scale = (y_max - y_min) / (height/3)

    # Loop through each x pixel
    for x_pixel in range(width):
        # Convert the pixel x-coordinate to the mathematical x-value
        x_value = x_min + x_pixel * x_scale

        # Calculate the corresponding y-value for the function
        y_value = func(x_value)

        # Scale the y-value to the display height and invert it (because displays usually have y=0 at the top)
        y_pixel = int(height - (y_value - y_min) / y_scale)

        # Ensure y_pixel is within the display range
        if 0 <= y_pixel < height:
            fb.pixel(x_pixel, y_pixel, 1)

# fb.fill(0)

# # Draw a pixel at (10, 10)
# fb.pixel(10, 10, 1)

# # Draw a line from (0, 0) to (127, 63)
# fb.line(0, 0, 127, 63, 1)

# # Draw a rectangle at (20, 20) with width 40 and height 20
# fb.rect(20, 20, 40, 20, 1)

# # Write text at (30, 30)
# fb.text("Hello", 30, 30, 1)

# fb.fill(0)

def polynom(x):
    y=math.sin(x)
    return y
# x=0
# y=x**2
# fb.line(0,31,127,31, 1)
# fb.line(63,0,63,63)
for i in range(0,8):
    y=63-i**2
    fb.pixel(i, y, 1)
fb.fill(0)

plot_function(fb, polynom, 0, 2, -1, 1, 128, 64)

print("")
print("")
binary_visual_list = bytearray_to_binary_visual_list(buffer)
# print(binary_visual_list) 

def update_display():
    for page in range(8):  # ST7565R has 8 pages (for 64 pixels in height, each page is 8 pixels)
        set_page_address(page)
        set_column_address(0)
        # CS1.value(0)  # Select the display
        for i in range(128):  # Send all 128 columns of the current page
            # write_data(bytearray([buffer[page * 128 + i]]))
            write_data(eval(binary_visual_list[page * 128 + i]))
            # spi.write(bytearray([buffer[page * 128 + i]]))
        # CS1.value(1)  # Deselect the display

# # Example: after drawing, call update_display() to refresh the display with the current buffer
update_display()

# for k in range(0,5):

#     for i in range(0,8):
#         for j in range(0,8):
#             set_page_address(i)
#             set_column_address(i*8+j+16*k)
#             write_data(0b10101010)

# for i in range(0,8):
#     for j in range(0,128):
#         set_page_address(i)
#         set_column_address(j)
#         write_data(0b11110000)
