#pragma once
#include <WiFi.h>
#include <WiFiClient.h>
#include <ESPmDNS.h>

class SensorClient {
public:
    SensorClient(const char* serverName, uint16_t serverPort);

    bool connect();
    bool isConnected();

    void sendPut(uint8_t interval);      // PUT command
    bool getIntervals(uint8_t varId);    // GET commando for intervals
    bool receiveInterval(uint8_t &interval); // Get valid values from server

private:
    WiFiClient wifiClient;
    IPAddress serverIP;
    const char* serverName;
    uint16_t serverPort;
};
