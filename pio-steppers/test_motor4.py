from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys

@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
         out_init=(PIO.OUT_LOW,) * 4,
         out_shiftdir=PIO.SHIFT_RIGHT,
         in_shiftdir=PIO.SHIFT_LEFT)
def prog():
    pull()
    mov(x, osr) # num steps
    
    pull()
    mov(y, osr) # step pattern
    
    jmp(not_x, "end")
    
    label("loop")
    jmp(not_osre, "step") # loop pattern if exhausted
    mov(osr, y)
    
    label("step")
    out(pins, 4) [31]
    
    jmp(x_dec,"loop")
    label("end")
    
    irq(rel(0))


sm = StateMachine(0, prog, freq=10000, set_base=Pin(2), out_base=Pin(2))
data = [(1,2,4,8),(2,4,8,1),(4,8,1,2),(8,1,2,4)]
steps = 0

def turn(sm):
    global steps
    global data
    
    idx = steps % 4
    a = data[idx][0] | (data[idx][1] << 4) | (data[idx][2] << 8) | (data[idx][3] << 12)
    a = a << 16 | a
    
    #print("{0:b}".format(a))
    sleep(1)
    
    sm.put(500)
    sm.put(a)
    
    steps += 500

sm.irq(turn)
sm.active(1)
turn(sm)

sleep(50)
print("done")
sm.active(0)
sm.exec("set(pins,0)")





