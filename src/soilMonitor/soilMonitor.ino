#include <ArduinoJson.h>

const int AirValue = 620;
const int WaterValue = 310;
const int med_low=369;
const int med_high=700;

int soilMoistureValue = 0;
int soilmoisturepercent=0;
int potReading;
String potVal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) {
  }
  int start = Serial.parseInt();
  soilMoistureValue = analogRead(A0);  //put Sensor insert into soil
  potReading = analogRead(A2);
  
  //Decide which watering type it is (chooses how much water to add and what is considered a thirsty plant)
  if(potReading < med_low) potVal = "LOW";
  else if(potReading < med_high) potVal = "MEDIUM";
  else potVal = "HIGH";

  soilmoisturepercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);
  
  if(soilmoisturepercent >= 100)
  {
    soilmoisturepercent = 100;
  }
  else if(soilmoisturepercent <= 0)
  {
    soilmoisturepercent = 0;
  }
  // Create the JSON document
  StaticJsonDocument<200> doc;
  doc["moisture"] = soilmoisturepercent;
  doc["temperature"] = "19";
  doc["watered"] = false;
  doc["plantWaterType"] = potVal;

  // Send the JSON document over the "link" serial port
  serializeJson(doc, Serial);
  delay(1000);
}
