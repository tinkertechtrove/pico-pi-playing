from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys

@asm_pio(set_init=(PIO.OUT_LOW,) * 4)
def prog():
    wrap_target()
    set(pins, 8) [31] # 8
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 4) [31] # 4
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 2) [31] # 2
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 1) [31] # 1
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    wrap()
    

sm = StateMachine(0, prog, freq=100000, set_base=Pin(2))


sm.active(1)
sleep(50)
sm.active(0)
sm.exec("set(pins,0)")
