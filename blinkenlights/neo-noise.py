# Example using PIO to drive a set of WS2812 LEDs.

import array, time
from machine import Pin
import rp2

# Configure the number of WS2812 LEDs.
NUM_LEDS = 32 * 8
PIN_NUM = 16
brightness = 0.3

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

def color_chase(color, wait):
    for i in range(NUM_LEDS):
        pixels_set(i, color)
        time.sleep(wait)
        pixels_show()
    time.sleep(0.2)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
        time.sleep(wait)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0) 
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

#print("fills")
#for color in COLORS:
#    pixels_fill(color)
#    pixels_show()
#    time.sleep(0.2)

#print("chases")
#for color in COLORS:
#    color_chase(color, 0.01)

#print("rainbow")
#rainbow_cycle(0)


#-------
# Worley Noise Generator
# http://en.wikipedia.org/wiki/Worley_noise
# FB36 - 20130216
import math
import gc
import random

# -----

def HueToRGB(h, s=1, v=1):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist


# ---

imgx = 32; imgy = 8# image size

pixels = [(0,0,0) for x in range(imgx*imgy)]
n = 4 # of seed points
m = 0 # random.randint(0, n - 1) # degree (?)
seedsX = [random.randint(0, imgx - 1) for i in range(n)]
seedsY = [random.randint(0, imgy - 1) for i in range(n)]
dirsX = [1 for i in range(n)]
dirsY = [1 for i in range(n)]

pixels_fill(BLACK)
pixels_show()

while True:
    #time.sleep(0.1)
    for i in range(n):
        seedsX[i] = seedsX[i] + dirsX[i]
        if seedsX[i] >= imgx:
            dirsX[i] = -1
        if seedsX[i] <= 0:
            dirsX[i] = 1
            
        seedsY[i] = seedsY[i] + dirsY[i]
        if seedsY[i] >= imgy:
            dirsY[i] = -1
        if seedsY[i] <= 0:
            dirsY[i] = 1
    
    # find max distance
    maxDist = 0.0
    for ky in range(imgy):
        for kx in range(imgx):
            # create a sorted list of distances to all seed points
            dists = [calculateDistance(seedsX[i], seedsY[i], kx, ky) for i in range(n)]
            dists.sort()
            if dists[m] > maxDist: maxDist = dists[m]

    # paint
    for ky in range(imgy):
        for kx in range(imgx):
            # create a sorted list of distances to all seed points
            dists = [calculateDistance(seedsX[i], seedsY[i], kx, ky) for i in range(n)]
            dists.sort()
            c = int(round(255 * dists[m] / maxDist))
            pixels[ky * imgx + kx] = HueToRGB(c)
            dists = None
            #gc.collect()

    for y in range(imgy/2):
        for x in range(imgx):
            #pixels_set((y*2)*imgx+x, RED)
            pixels_set((y*2)*imgx+x, pixels[y * imgx + x])
            
        for x in range(imgx):
            pixels_set((y*2+1)*imgx+x, pixels[y * imgx + (imgx - x - 1)])
            
            #else:
            #    pixels_set(y*imgx+x, BLACK)
                
    pixels_show()
