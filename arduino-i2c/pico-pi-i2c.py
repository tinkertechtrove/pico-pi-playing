 
from machine import Pin, I2C
from time import sleep

MSG_SIZE = 15

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000) 
addr = i2c.scan()[0]

i2c.writeto(addr, 'Hi from Pi')
sleep(0.1)
a = i2c.readfrom(addr, MSG_SIZE)
print(a)

print("done")