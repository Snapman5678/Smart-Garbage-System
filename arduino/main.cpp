#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_DHT.h>

#define TRIG_PIN 4   // HC-SR04 Trig pin
#define ECHO_PIN 3   // HC-SR04 Echo pin

#define DHT_PIN 2    // DHT11 data pin

#define MQ_PIN A3    // MQ-4 analog output pin

#define DHT_TYPE DHT11   // DHT sensor type

DHT dht(DHT_PIN, DHT_TYPE);

bool binFilled = false; // Flag to track if the bin is filled

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  dht.begin();
}

float readTemperature() {
  return dht.readTemperature();
}

float readHumidity() {
  return dht.readHumidity();
}

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2;
  return distance;
}

float readGasConcentration() {
  int sensorValue = analogRead(MQ_PIN);
  float voltage = sensorValue * (5.0 / 1023.0);
  
  // Convert voltage to gas concentration (example calibration)
  float gasConcentration = 2.0 * voltage;
  return gasConcentration;
}

void loop() {
  float distance = readDistance();

  if (!binFilled && distance < 20) { // Check if bin is not filled and distance is less than 20 cm
    binFilled = true; // Set the bin filled flag
    delay(5000); // Wait for 5 seconds
    float temperature = readTemperature();
    float humidity = readHumidity();
    float gasConcentration = readGasConcentration();
  
    // Determine type of waste based on sensor readings
    String wasteType = determineWasteType(temperature, humidity, gasConcentration);
  
    // Print sensor readings and waste type
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print("°C\t Humidity: ");
    Serial.print(humidity);
    Serial.print("%\t Distance: ");
    Serial.print(distance);
    Serial.print(" cm\t Gas Concentration: ");
    Serial.print(gasConcentration);
    Serial.print(" ppm\t Waste Type: ");
    Serial.println(wasteType);
  
    // Send waste type over serial port
    Serial.println(wasteType);
  }
  
  if (binFilled && distance > 20) { // Check if bin was filled but now distance is greater than 20 cm
    binFilled = false; // Reset the bin filled flag
  }

  delay(1000); // Delay between readings
}

String determineWasteType(float temperature, float humidity, float gasConcentration) {
  if (humidity > 50 && gasConcentration > 100) {
    return "Wet Waste";
  } else {
    return "Dry Waste";
  }
}
