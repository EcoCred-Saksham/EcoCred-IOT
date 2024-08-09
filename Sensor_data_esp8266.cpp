#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Constants
const int mq135Pin = A0;  // Analog pin connected to MQ-135

// Calibration parameters
float R0 = 10.0; // The baseline resistance of the sensor in clean air

// Function to read MQ-135 sensor and calculate CO2 concentration
float readMQ135() {
  int sensorValue = analogRead(mq135Pin);
//  float sensorVoltage = sensorValue * (3.3 / 1023.0);  // Convert analog value to voltage
//  float sensorResistance = (3.3 - sensorVoltage) / sensorVoltage;  // Calculate resistance
//  float ratio = sensorResistance / R0;  // Calculate ratio
//  // Use a formula to convert ratio to CO2 concentration (ppm)
//  float co2ppm = 116.6020682 * pow(ratio, -2.769034857);  // Example formula, adjust based on calibration
//  return co2ppm;
  return sensorValue;
}

const char* ssid = "SAKSHAM";
const char* password = "bdcoe123";
const char* serverUrl = "http://192.168.137.150:5000/data";

void setup() {
  Serial.begin(115200);
  pinMode(mq135Pin, INPUT);
//  // Calibration routine
//  Serial.println("Calibrating MQ-135 sensor...");
//  delay(20000); // Let the sensor settle
//  float sensorValue = analogRead(mq135Pin);
//  float sensorVoltage = sensorValue * (3.3 / 1023.0);
//  R0 = (3.3 - sensorVoltage) / sensorVoltage;
//  Serial.print("R0 value: ");
//  Serial.println(R0);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  float co2ppm = readMQ135();
  Serial.print("CO2 concentration: ");
  Serial.print(co2ppm);
  Serial.println(" ppm");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"value\":" +String(co2ppm)+ "}";

    int httpResponseCode = http.POST(jsonData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response code: " + String(httpResponseCode));
      Serial.println("Response: " + response);
    } else {
            String response = http.getString();

      Serial.println("HTTP Response code: " + String(httpResponseCode));
            Serial.println("Response: " + response);

      Serial.println("Error in sending POST request");
    }

    http.end();
  } else {
    
    Serial.println("WiFi Disconnected");
  }

  delay(2000);
}
