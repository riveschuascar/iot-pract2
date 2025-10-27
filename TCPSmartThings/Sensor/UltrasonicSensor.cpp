#include "UltrasonicSensor.h"

UltrasonicSensor::UltrasonicSensor(uint8_t trig, uint8_t echo)
    : trigPin(trig), echoPin(echo), lastInterval(2), actualInterval(2) 
{
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

double UltrasonicSensor::readDistanceCM() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    double duration = pulseIn(echoPin, HIGH, 30000); // >= 30 ms timeout
    if (duration == 0) return -1;
    return duration * 0.034 / 2;
}

double UltrasonicSensor::applySquareCalibration(double distance) {
    const double a = 0.0004888296644567358;
    const double b = 1.019077967700977;
    const double c = -0.9416840503467725;
    return a * distance * distance + b * distance + c;
}

double UltrasonicSensor::applyLinearCalibration(double distance) {
    const double a = 1.0529949029039745;
    const double b = -1.2453937040040843;
    return a * distance + b;
}

uint8_t UltrasonicSensor::distanceToInterval(double distance) {
    lastInterval = actualInterval;
    if (distance == -1) {
        actualInterval = 2;
    }
    else if (distance < 30) {
        actualInterval = 0;
    }
    else if (distance < 60) {
        actualInterval = 1;
    }
    else {
        actualInterval = 2;
    }
    return actualInterval;
}

bool UltrasonicSensor::hasIntervalChanged() {
    return actualInterval != lastInterval;
}
