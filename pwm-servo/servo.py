import time
from machine import Pin, PWM

MIN_DUTY = 1000 # 5 percent of 65025 = 3251.25
MAX_DUTY = 9000 # 10 percent of 65025 = 6502.5

pwm = PWM(Pin(0))
pwm.freq(50)

duty = MIN_DUTY
direction = 1

while True:
	for _ in range(1024):
		duty += direction
		if duty > MAX_DUTY:
			duty = MAX_DUTY
			direction = -direction
		elif duty < MIN_DUTY:
			duty= MIN_DUTY
			direction = -direction
		pwm.duty_u16(duty)