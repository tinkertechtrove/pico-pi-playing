At the time of writing this (Sun 20 Jun 14:31:47 BST 2021) there is a library issue
that prevents this demo from working without modifying either the Adafruit Neopixel
library (easier) or the PDM library thats part of the RP2040 connects board support
in the Arduino IDE (harder). Both libraries thing they can use PIO state machine 0.

To fix this, find the source for the Adafruit library 
`(~/Arduino/libraries/Adafruit_NeoPixel)` for me. And change it to use state machine
1. Edit `rp2040.c` and set `int sm` to 1 on line 22. Next change the call on line 51
to use 1 instead of 0 (or put this in variable and use it in both places). 

