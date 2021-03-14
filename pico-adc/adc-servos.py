from machine import ADC, PWM, Pin
from time import sleep


MIN_DUTY = 3000 # 5 percent of 65025 = 3251.25
MAX_DUTY = 6000 # 10 percent of 65025 = 6502.5

pwmX = PWM(Pin(0))
pwmX.freq(50)

pwmY = PWM(Pin(1))
pwmY.freq(50)

adcX = ADC(0)
adcY = ADC(1)
oldX = 0
oldY = 0

while True:
    valX = adcX.read_u16()
    valY = adcY.read_u16()
    if valX != oldX or valY != oldY:
        #print(MIN_DUTY + int((valX/65535) * MAX_DUTY))
        pwmX.duty_u16(MIN_DUTY + int((valX/65535) * MAX_DUTY))
        pwmY.duty_u16(MIN_DUTY + int((valY/65535) * MAX_DUTY))
        sleep(0.1)
        oldX = valX
        oldY = valY
