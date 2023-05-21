import I2C_LCD_driver
from time import *

# see explanation here
# https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
# identico
# https://wiki.52pi.com/index.php?title=1602_Serial_LCD_Module_Display_SKU:Z-0234

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("Nope!      Nope!", 1)