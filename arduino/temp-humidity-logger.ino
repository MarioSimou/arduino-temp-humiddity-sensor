#include <dht11.h>

int PIN_NUM=13;
long delaySec= 1200000;

dht11 DHT11;

void setup(){
  Serial.begin(9600);  
}

void loop(){
  DHT11.read(PIN_NUM);  

  String json = "{\"temperature\":" + String(DHT11.temperature) + ",\"humidity\":" + String(DHT11.humidity) + "}";
  Serial.print(json);
  delay(delaySec);
}
