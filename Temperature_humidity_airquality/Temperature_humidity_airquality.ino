/////Inside humidity and temperature///////
#include "DHT.h"             // DHT sensors library
#define dhtPin 8             // This is data pin
#define dhtType DHT22        // This is DHT 22 sensor
DHT dht(dhtPin, dhtType);    // Initialising the DHT library
float humValue;           // value of humidity
float temperatureValueC;  // value of temperature in degrees Celcius
///////Inside humidity and temperature///////

//////Inside Air Quality//////
int airQuality = A0;
int co2Level;
//////Inside Air Quality//////

/////Outside humidity and temperature///////
#define dhtPin1 7             // This is data pin
#define dhtType1 DHT22        // This is DHT 22 sensor
DHT dht1(dhtPin1, dhtType1);    // Initialising the DHT library
float humValue1;           // value of humidity
float temperatureValueC1;  // value of temperature in degrees Celcius
///////Outside humidity and temperature///////

//////Outside Air Quality//////
int airQuality1 = A1;
int co2Level1;
//////Outside Air Quality//////

void setup(){
  Serial.begin(9600);
///////Inside humidity and temperature///////
  dht.begin();               // start reading the value from DHT sensor
///////Inside humidity and temperature///////

///////Inside humidity and temperature///////
  dht1.begin();               // start reading the value from DHT sensor
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

//////Inside Air Quality//////
  int airQualityData = analogRead(airQuality);
  co2Level = airQualityData - 112;
  co2Level = map(co2Level,0,1024,400,5000);
  Serial.print(" , ");
  Serial.print(co2Level);
//////Inside Air Quality//////

///////Outside humidity and temperature///////
  humValue1 = dht1.readHumidity();               // value of humidity
  temperatureValueC1 = dht1.readTemperature();   // value of temperature in degrees Celcius
  Serial.print(" , ");
  Serial.print(humValue1);     // get value of humidity
  Serial.print(" , ");          // create space after the value of humidity
  Serial.print(temperatureValueC1);  // get value of temperature in degrees Celcius
///////Outside humidity and temperature///////

//////Outside Air Quality//////
  int airQualityData1 = analogRead(airQuality1);
  co2Level1 = airQualityData1 - 112;
  co2Level1 = map(co2Level1,0,1024,400,5000);
  Serial.print(" , ");
  Serial.println(co2Level1);
//////Outside Air Quality//////

  delay(10000);
}
