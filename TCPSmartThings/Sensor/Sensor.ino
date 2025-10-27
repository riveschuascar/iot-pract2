#include "WifiManager.h"
#include "UltrasonicSensor.h"
#include "SensorClient.h"

UltrasonicSensor sensor(27, 26);
WifiManager wifiManager("UCB-PREMIUM", "lacatoucb");
SensorClient server("iot.server", 10000);

void setup() {
  Serial.begin(115200);
  wifiManager.begin();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi desconectado. Intentando reconectar...");
    wifiManager.begin();
    delay(1000);
    return;
  }

  if (!server.connect()) {
    delay(1000);
    return;
  }

  double distance = sensor.readDistanceCM();
  double calibratedSqrDistance = sensor.applySquareCalibration(distance);
  double calibratedLinDistance = sensor.applyLinearCalibration(distance);
  Serial.printf("%f,%f,%f\n", distance, calibratedSqrDistance, calibratedLinDistance);

  // Para intervalos
  uint8_t interval = sensor.distanceToInterval(distance);

  if (sensor.hasIntervalChanged()) {
    Serial.printf("Distance: %f cm -> Interval: %u\n", distance, interval);
    server.sendPut(interval);  // send "PUT" to server
  }

  delay(330);
}
