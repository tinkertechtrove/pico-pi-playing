from machine import UART, Pin
from time import sleep
import struct

uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) # UART tx/rx
ready = Pin(3, Pin.IN, Pin.PULL_DOWN) # used to check the ESP01 status
reset = Pin(2, Pin.OUT) # used to wake the ESP01 from deep sleep

reset.value(1) # ESP01 reset pin, high in normal mode, low to reset  


def send_message(msg):
    print("Send msg ....")
    uart0.write(b'msg')
    uart0.write(struct.pack('!I', len(msg)))
    uart0.write(msg)

    # read the header
    rxData = bytes()
    while len(rxData) < 7: # add timeout ...
        while uart0.any() > 0:
            rxData += uart0.read(1)
            
    # decode the header
    if rxData[0:3] == b'msg':
        size = struct.unpack_from('!I', rxData, 3)[0]
    else:
        return '' # we dont understand the message
        
    # read the full message
    while len(rxData) < size + 7:
        while uart0.any() > 0:
            rxData += uart0.read(1)
            
    return rxData[7:].decode('utf-8')

def esp01_ready():
    while ready.value() == 0:
        print('.', end ="")
        sleep(0.1)
        
    for i in range(4):
        while uart0.any():
            uart0.read(1) # empty any boot up data
        sleep(0.1)
    
    print("Ready")


def esp01_sleep():
    print('sleep')
    send_message('sleep')
    while ready.value() == 1:
        print('.', end="")
        sleep(0.1)
    print('ok')
    

def esp01_wake():
    print("wake")
    reset.value(0)
    sleep(0.1)
    reset.value(1)
    esp01_ready()



esp01_ready()
while True:
    sleep(10)
    print("Message:", send_message('http://192.168.1.237'))
    esp01_sleep()
    sleep(10)
    esp01_wake()
    
    
