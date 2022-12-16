/////Inside humidity and temperature///////
#include "DHT.h"             // DHT sensors library
#define dhtPin 8             // This is data pin
#define dhtType DHT22        // This is DHT 22 sensor
DHT dht(dhtPin, dhtType);    // Initialising the DHT library
float humValue;           // value of humidity
float temperatureValueC;  // value of temperature in degrees Celcius
///////Inside humidity and temperature///////

//////Air Quality//////
int airQuality = A0;
int co2Level;
//////Air Quality//////

void setup(){
  Serial.begin(9600);
///////Inside humidity and temperature///////
  dht.begin();               // start reading the value from DHT sensor
///////Inside humidity and temperature///////

}

void loop() {
///////Inside humidity and temperature///////
  humValue = dht.readHumidity();               // value of humidity
  temperatureValueC = dht.readTemperature();   // value of temperature in degrees Celcius
  Serial.print(humValue);     // get value of humidity
  Serial.print(" , ");          // create space after the value of humidity
  Serial.print(temperatureValueC);  // get value of temperature in degrees Celcius
///////Inside humidity and temperature///////

//////Air Quality//////
  int airQualityData = analogRead(airQuality);
  co2Level = airQualityData - 112;
  co2Level = map(co2Level,0,1024,400,5000);
  Serial.print(" , ");
  Serial.println(co2Level);
//////Air Quality//////
 
  delay(1000);
}
