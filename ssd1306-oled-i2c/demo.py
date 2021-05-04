from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

w = 128
h = 32

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=200000)
addr = i2c.scan()[0]
oled = SSD1306_I2C(w, h, i2c, addr)

# Add some text
oled.fill(0)
oled.text("Raspberry Pi ", 5, 5)
oled.text("Pico ssd1306", 5, 15)
oled.show()


