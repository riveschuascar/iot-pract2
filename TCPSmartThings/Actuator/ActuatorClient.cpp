#include "ActuatorClient.h"

#define CMD_REGISTER 0x03
#define CMD_COMMAND 0x04

ActuatorClient::ActuatorClient(const char* serverName, uint16_t serverPort)
  : serverName(serverName), serverPort(serverPort), serverIP(INADDR_NONE) {}

bool ActuatorClient::connect() {
  if (!wifiClient.connected()) {
    int n = MDNS.queryService("_server", "_tcp");
    if (n > 0) {
      Serial.printf("Found %d _iot._tcp services:\n", n);
      for (int i = 0; i < n; i++) {
        IPAddress ip = MDNS.address(i);
        uint16_t port = MDNS.port(i);
        Serial.printf("%d: Host=%s, IP=%s, Port=%u\n",
                      i, MDNS.hostname(i).c_str(),
                      ip.toString().c_str(), port);

        if (wifiClient.connect(ip, port)) {
          Serial.println("Connected to server via mDNS!");
          return true;
        }
      }
      Serial.println("Failed to connect to any _server._tcp service, retrying...");
      return false;
    } else {
      Serial.println("No _server._tcp services found, retrying...");
      return false;
    }
  }
  return true;
}

bool ActuatorClient::isConnected() {
  return wifiClient.connected();
}

void ActuatorClient::registerActuator() {
  if (wifiClient.connected()) {
    wifiClient.write(CMD_REGISTER);
    Serial.println("Sent REGISTER to server");
  }
}

void ActuatorClient::handle() {
  while (wifiClient.connected() && wifiClient.available() >= 1) {
    uint8_t cmd = wifiClient.read();

    if (cmd == CMD_COMMAND) {
      // esperar el byte LEN
      if (wifiClient.available() < 1) break;
      uint8_t len = wifiClient.read();

      // esperar los bytes de DATA
      if (wifiClient.available() < len) break;

      uint8_t interval = wifiClient.read();  // solo hay 1 byte en este caso
      if (interval <= 2) {
        currentInterval = interval;
        Serial.printf(">> Intervalo recibido del servidor: %d\n", interval);
      } else {
        Serial.printf("Intervalo inválido: %d\n", interval);
      }
    } else {
      Serial.printf("Comando desconocido: 0x%02X\n", cmd);
    }
  }
}

uint8_t ActuatorClient::getCurrentInterval() {
  return currentInterval;
}
