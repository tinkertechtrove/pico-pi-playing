
#include <Wire.h>

#define UNO_ADDR 9
#define RESP_SIZE 15

String data = "Hi from Arduino";

void setup()
{
  Serial.begin(9600);
  Wire.begin(UNO_ADDR);
  /*Event Handlers*/
  Wire.onReceive(DataReceive);
  Wire.onRequest(DataRequest);
}

void loop()
{
  delay(50);
}

void DataReceive(int numBytes)
{
  int i=0;
  char data[RESP_SIZE];
  memset(data,0, RESP_SIZE);
  while(Wire.available()) 
  { 
    data[i++] = Wire.read();
  }
  
  Serial.println("Recv Event");
  Serial.println(String(data));
}

void DataRequest()
{
  byte resp[RESP_SIZE];
  for (byte i=0; i<RESP_SIZE; ++i) {
    resp[i] = (byte)data.charAt(i);
  }
  Wire.write(resp, sizeof(resp));
  Serial.println("Sent resp");
}
