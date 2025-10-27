#include "WifiManager.h"
#include "Servo360.h"
#include "ActuatorClient.h"

WifiManager wifiManager("UCB-PREMIUM", "lacatoucb");
Servo360 servo(25);
ActuatorClient actuator("iot.server.local", 10000);
uint8_t lastInterval = 2;

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

  if (!actuator.connect()) {
    delay(1000);
    return;
  }

  actuator.handle();

  uint8_t current = actuator.getCurrentInterval();
  if (current != lastInterval) {
    servo.setInterval(current);
    Serial.printf("Nuevo intervalo aplicado: %d\n", current);
    lastInterval = current;
  }

  servo.update();
  delay(20);
}
