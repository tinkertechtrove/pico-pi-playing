

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define GPIO_STATUS 2

// This was tested on an ESP-01s. Users of non-S varient ESP-01 modules have reported
// needing to change "Builtin Led" in the sketch tools menu from "2" to "1"


void setup() {
  Serial.begin(115200);   // Serial UART boardrate

  // status pin GPIO2
  pinMode(GPIO_STATUS, OUTPUT);
  digitalWrite(GPIO_STATUS, LOW);
  pinMode(LED_BUILTIN, OUTPUT); // to flash the LED

  // WiFi details - note this does not handle reconnection
  WiFi.mode(WIFI_STA);
  WiFi.begin("SSID", "PASSWORD");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  digitalWrite(GPIO_STATUS, HIGH); // set status to say we are online
  Serial.flush();
}

void send(const char* data) {
  if(data){
    unsigned int len = htonl(strlen(data));
    Serial.write("msg");
    Serial.write((char*)&len, 4);
    Serial.write(data);
    Serial.flush();
  }
}

void fetch(char* url) {
  WiFiClient client;
  HTTPClient http;

  digitalWrite(LED_BUILTIN, LOW); // turn on the LED
  if (http.begin(url)) {  // HTTP
    int httpCode = http.GET();
    if (httpCode > 0) { // httpCode will be negative on error
      if (httpCode == HTTP_CODE_OK) {
        send(http.getString().c_str());
      }
    } else {
      send(http.errorToString(httpCode).c_str());
    }
    http.end();
  } else {
    send("[HTTP] Unable to connect\n");
  }
  digitalWrite(LED_BUILTIN, HIGH); // turn off the LED
}

char buf[128];
char* read_message() {
  if(!Serial.available()) {
    return NULL;
  }
  
  int idx = 0;
  memset(buf, 0, 128);
  while(idx < 7) {
    while(Serial.available() > 0) {    // Checks is there any data in buffer (holds 64 bytes max)
      buf[idx++] = char(Serial.read());           // Read serial data byte
    }
  }
  
  if(memcmp(buf, "msg", 3) == 0) {
    unsigned int size = ntohl(*(unsigned int*)(buf + 3)); 
    while(idx < size + 7 && idx < 120) {
      while(Serial.available() > 0) {   
        buf[idx++] = char(Serial.read());
      }
    }
  } else {
    return NULL;
  }

  return buf + 7;
}


void loop() {
  char* msg = read_message();
  if(msg) {
    if(memcmp(msg, "sleep", 5) == 0) {
      send("ok");
      digitalWrite(2, LOW);
      ESP.deepSleep(0, WAKE_RF_DEFAULT); // go to sleep
    } else {
      fetch(msg);
    }
  }
}
