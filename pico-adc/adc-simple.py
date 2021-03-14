from machine import ADC, Pin
from time import sleep

adcX = ADC(0)
adcY = ADC(1)
oldX = 0
oldY = 0

while True:
    valX = adcX.read_u16()
    valY = adcY.read_u16()
    sleep(0.5)
    if valX != oldX or valY != oldY:
        print("X:", valX, " Y:", valY)
        oldX = valX
        oldY = valY