from machine import I2C, Pin # type: ignore
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# Define the I2C bus
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Define the LCD address and size (e.g., 0x27 for a 16x2 LCD)
I2C_ADDR = 0x27
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Initialize the LCD
lcd.clear()
lcd.move_to(0, 0)

# Display a backslash
lcd.putstr("This is a backslash: \\")

# If you need to move to a new line or position, use move_to(row, col)
lcd.move_to(0, 1)
lcd.putstr("Another backslash: \\")
