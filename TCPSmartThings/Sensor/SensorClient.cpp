#include "SensorClient.h"

#define CMD_PUT 0x01
#define CMD_GET 0x02

SensorClient::SensorClient(const char* serverName, uint16_t serverPort)
  : serverName(serverName), serverPort(serverPort), serverIP(INADDR_NONE) {}

bool SensorClient::connect() {
  if (!wifiClient.connected()) {
    // Find _server._tcp services in the local WiFi network
    int n = MDNS.queryService("_server", "_tcp");
    if (n > 0) {
      Serial.printf("Found %d _iot._tcp services:\n", n);
      for (int i = 0; i < n; i++) {
        IPAddress ip = MDNS.address(i);
        uint16_t port = MDNS.port(i);
        Serial.printf("%d: Host=%s, IP=%s, Port=%u\n",
                      i, MDNS.hostname(i).c_str(),
                      ip.toString().c_str(), port);

        // Try to connect to found host
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
  return true;  // already connected
}

bool SensorClient::isConnected() {
  return wifiClient.connected();
}

void SensorClient::sendPut(uint8_t interval) {
  if (wifiClient.connected()) {
    uint8_t buffer[3];
    buffer[0] = CMD_PUT; // 0x01 PUT Sensor->Server
    buffer[1] = 1;       // LEN = 1 byte
    buffer[2] = interval; 
    wifiClient.write(buffer, 3);
  }
}

bool SensorClient::getIntervals(uint8_t varId) {
  if (!wifiClient.connected()) return false;
  wifiClient.write(CMD_GET);  // 0x02 GET Server->Sensor
  wifiClient.write(varId);    // varId=1 para intervalos
  return true;
}

bool SensorClient::receiveInterval(uint8_t& interval) {
  if (!wifiClient.connected() || !wifiClient.available()) return false;
  interval = wifiClient.read();  // servidor envía un solo byte 0,1,2
  return true;
}
