#include "WifiManager.h"
#include "Servo360.h"
#include "ActuatorClient.h"

WifiManager wifiManager("", "");
Servo360 servo(25);
ActuatorClient actuator("iot.server.local", 10000);
uint8_t lastInterval = 2;

void setup() {
  Serial.begin(115200);
  servo.begin();
  wifiManager.begin();
}

void loop() {
    // 1. Mantener conexión Wi-Fi
    if (WiFi.status() != WL_CONNECTED) {
        wifiManager.begin();
        delay(1000);
        return;
    }

    // 2. Mantener conexión TCP solo si no está conectada
    if (!actuator.isConnected()) {
        actuator.connect();
        actuator.registerActuator();
    }

    // 3. Procesar mensajes pendientes
    actuator.handle();

    // 4. Actualizar servo si hay cambio
    uint8_t current = actuator.getCurrentInterval();
    if (current != lastInterval) {
        servo.setInterval(current);
        Serial.printf("Nuevo intervalo aplicado: %d\n", current);
        lastInterval = current;
    }

    // 5. Actualizar servo (sin bloquear)
    servo.update();
}
