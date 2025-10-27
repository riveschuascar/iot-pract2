#pragma once
#include <Arduino.h>

class UltrasonicSensor {
public:
    UltrasonicSensor(uint8_t trig, uint8_t echo);

    double readDistanceCM();
    double applySquareCalibration(double distance);
    double applyLinearCalibration(double distance);
    uint8_t distanceToInterval(double distance);
    bool hasIntervalChanged();

private:
    uint8_t trigPin;
    uint8_t echoPin;
    uint8_t lastInterval;
    uint8_t actualInterval;
};
