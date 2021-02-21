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
    mov(y, osr) # step pattern
    
    wrap_target()
    
    pull()
    mov(x, osr) # num steps
    
    mov(osr, y) # restore osr
    jmp(not_x, "end")
    
    label("loop")
    jmp(not_osre, "step") # loop pattern if exhausted
    mov(osr, y)
    
    label("step")
    out(pins, 4) [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    


    jmp(x_dec,"loop")
    label("end")
    
    
    # backup osr - this is broken
    #mov(isr, y)
    in_(y,32)
    label("bu_jump")
    in_(osr, 1)
    out(null, 1)
    jmp(not_osre, "bu_jump")
    mov(y, isr)
    
    irq(rel(0))
    push()


sm = StateMachine(0, prog, freq=0, set_base=Pin(2), out_base=Pin(2))

def turn(sm):
    a = sm.get()
    print("{0:b}".format(a))
    sleep(1)
    sm.put(1)
    print("irq")

sm.irq(turn)
sm.active(1)
sm.put(2216789025) #1000 0100 0010 0001   1000 0100 0010 0001
                   #1000 0100 0010 0001   1000 0100 1000 0100
                   #1000 0100 0010 0001   1000 0100 1000 0100
sm.put(1)

sleep(50)
print("done")
sm.active(0)
sm.exec("set(pins,0)")



