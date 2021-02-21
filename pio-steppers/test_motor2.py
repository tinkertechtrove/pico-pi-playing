from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys

@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
         out_init=(PIO.OUT_HIGH,) * 4,
         out_shiftdir=PIO.SHIFT_LEFT)
def prog():
    pull()
    mov(y, osr) # step pattern
    
    pull()
    mov(x, osr) # num steps
    
    jmp(not_x, "end")
    
    label("loop")
    jmp(not_osre, "step") # loop pattern if exhausted
    mov(osr, y)
    
    label("step")
    out(pins, 4) [31]
    nop() [31]
    nop() [31]
    nop() [31]

    jmp(x_dec,"loop")
    label("end")
    set(pins, 8) [31] # 8



sm = StateMachine(0, prog, freq=10000, set_base=Pin(2), out_base=Pin(2))

sm.active(1)
sm.put(2216789025) #1000 0100 0010 0001 1000010000100001
sm.put(1000)
sleep(5)
sm.active(0)
sm.exec("set(pins,0)")



