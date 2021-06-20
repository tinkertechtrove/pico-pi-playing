
#include <Adafruit_NeoPixel.h>
#include <PDM.h>

#define CHANS 1
#define PCM_FREQ 16000;

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[512];

// Number of audio samples read
volatile int samplesRead;


#define LED_PIN    25
#define LED_COUNT  20
#define BRIGHTNESS 50 // Set BRIGHTNESS to about 1/5 (max = 255)

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_RGBW + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)


void setup() {
  //pinMode(LED_PIN, OUTPUT);
  strip.begin();
  strip.show();
  strip.setBrightness(BRIGHTNESS);
  
  Serial.begin(9600);

  // Configure the data receive callback
  PDM.onReceive(onPDMdata);
  PDM.setGain(-20); // Optionally set the gain

  // Initialize PDM with:
  if (!PDM.begin(CHANS, PCM_FREQ)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }

}

void loop() {
  uint32_t col = strip.Color(0, 0, 0);
  for(int i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, col); 
    delay(1);
  }
  
  if(samplesRead) {  // Wait for samples to be read
    int sampMax = 0;
    for (int i = 0; i < samplesRead; i++) {
      sampMax = max(sampMax, abs(sampleBuffer[i]));
    }
    
    int t = (int)((sampMax/32767.0f)*strip.numPixels());
    for(int i=0; i<t; i++) {
      int x = (int)((255.0/LED_COUNT) * i);
      col = strip.Color(255 - x, x, 0);
      strip.setPixelColor(i, col);
      delay(1);
    }
    
    samplesRead = 0;
  }
  strip.show();
  delay(10);
}

/**
 * Callback function to process the data from the PDM microphone.
 * NOTE: This callback is executed as part of an ISR.
 * Therefore using `Serial` to print messages inside this function isn't supported.
 * */
void onPDMdata() {
  // Query the number of available bytes
  int bytesAvailable = PDM.available();

  // Read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;
}
