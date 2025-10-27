#pragma once
#include <Arduino.h>
#include <WiFi.h>
#include <ESPmDNS.h>

class ActuatorClient {
public:
    ActuatorClient(const char* serverName, uint16_t serverPort);

    bool connect();
    bool isConnected();
    void registerActuator();

    void handle();                 // <-- nuevo: procesa mensajes entrantes
    uint8_t getCurrentInterval();  // <-- nuevo: retorna el valor más reciente

private:
    const char* serverName;
    uint16_t serverPort;
    IPAddress serverIP;
    WiFiClient wifiClient;

    uint8_t currentInterval = 2;   // 2 = STOP por defecto
};
