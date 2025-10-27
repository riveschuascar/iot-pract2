#pragma once
#include <WiFi.h>
#include <ESPmDNS.h>

class WifiManager {
public:
    WifiManager(const char* ssid, const char* password);
    void begin();

private:
    const char* ssid;
    const char* password;
};
