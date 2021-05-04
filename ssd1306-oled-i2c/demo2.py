from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C

w = 128
h = 32

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=200000)
addr = i2c.scan()[0]
oled = SSD1306_I2C(w, h, i2c, addr)

adcX = ADC(1)
adcY = ADC(2)

while True:
    valX = adcX.read_u16()
    valY = adcY.read_u16()
    
    x = (5 + (valX/65535) * (w-10));
    y = (5 + (valY/65535) * (h-10));
    
    oled.fill(0)
    oled.text("*", int(x), int(y))
    oled.show()


