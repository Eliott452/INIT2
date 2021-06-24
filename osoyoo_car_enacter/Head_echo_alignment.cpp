/*
  Head_echo_alignment.h - library for Osoyoo car align head towards closest ultrasonic echo.
  Created by Olivier Georgeon, june 20 2021
  released into the public domain
*/
#include "Arduino.h"
#include "head_echo_alignment.h"
#include <Servo.h>

#define SERVO_PIN   13  //servo connect to D5
#define Echo_PIN    31 // Ultrasonic Echo pin connect to A5
#define Trig_PIN    30  // Ultrasonic Trig pin connect to A4

Head_echo_alignment::Head_echo_alignment()
{
  //Servo _head;
  _is_enacting_head_alignment = false;
  _penultimate_ultrasonic_measure = 0;
  _previous_ultrasonic_measure = 1;
  _min_ultrasonic_measure = 0;
  _next_saccade_time = 0;
  _head_angle = 90;
  _head_angle_span = SACCADE_SPAN;
}

void Head_echo_alignment::setup()
{
  // init HC-SR04 ultrasonic Echo sensor
  pinMode(Trig_PIN, OUTPUT);
  pinMode(Echo_PIN,INPUT);
  digitalWrite(Trig_PIN,LOW);
  // init servo
  _head.attach(SERVO_PIN);
  _head.write(_head_angle);
}

void Head_echo_alignment::begin()
{
  _is_enacting_head_alignment = true;
  _penultimate_ultrasonic_measure = 0; // Reinitialize previous measures so it will not ...
  _previous_ultrasonic_measure = 1;    // ... believe that the next measure is a minimum
}

bool Head_echo_alignment::update()
{
  if (_is_enacting_head_alignment)
  {
    if (_next_saccade_time < millis()) {
      _next_saccade_time = millis() + SACCADE_DURATION;
      int current_ultrasonic_measure = measureUltrasonicEcho();
      Serial.println("Angle " +String(_head_angle) + " measure " + String(current_ultrasonic_measure));
      if (_previous_ultrasonic_measure > current_ultrasonic_measure ) {
        // Moving closer
        if ((_head_angle > 10) && (_head_angle < 170)) {
          _head_angle += _head_angle_span;
          _head.write(_head_angle);
        } else {
          _min_ultrasonic_measure = current_ultrasonic_measure;
          Serial.println("Aligned at edge angle " + String(_head_angle) + " measure " + String(_min_ultrasonic_measure));
          _is_enacting_head_alignment = false;
        }
      } else {
        // moving away, reverse movement
        _head_angle_span = - _head_angle_span;
        _head_angle += _head_angle_span;
        _head.write(_head_angle);
        if (_penultimate_ultrasonic_measure >= _previous_ultrasonic_measure) {
          // Passed the minimum, stop
          _min_ultrasonic_measure = _previous_ultrasonic_measure;
          Serial.println("Aligned at angle " + String(_head_angle) + " measure " + String(_min_ultrasonic_measure));
          _is_enacting_head_alignment = false;
          _head_angle_span = - _head_angle_span;
        }
      }
      _penultimate_ultrasonic_measure = _previous_ultrasonic_measure;
      _previous_ultrasonic_measure = current_ultrasonic_measure;
    }
  }
  return _is_enacting_head_alignment;
}

String Head_echo_alignment::outcome()
{
  return "A" + String(_head_angle) + "O" + String(_min_ultrasonic_measure);
}

bool Head_echo_alignment::monitor()
{
  if (!_is_enacting_head_alignment && _next_saccade_time < millis())
  {
    _next_saccade_time = millis() + ECHO_MONITOR_PERIOD;
    int current_ultrasonic_measure = measureUltrasonicEcho();
    //Serial.println("Angle " +String(_head_angle) + " measure " + String(current_ultrasonic_measure));
    if (abs(current_ultrasonic_measure - _min_ultrasonic_measure) > ECHO_MONITOR_VARIATION) {
      begin();
    }
  }
  return _is_enacting_head_alignment;
}

void Head_echo_alignment::turnHead(int head_angle)
{
  _head_angle = head_angle;
  _head.write(_head_angle);
}

int Head_echo_alignment::measureUltrasonicEcho()
{
  long echo_distance;
  digitalWrite(Trig_PIN,LOW);
  delayMicroseconds(5);
  digitalWrite(Trig_PIN,HIGH);
  delayMicroseconds(15);
  digitalWrite(Trig_PIN,LOW);
  echo_distance=pulseIn(Echo_PIN,HIGH);
  echo_distance=echo_distance * 0.1657; //how far away is the object in mm
  //Serial.print("Echo measure (mm): ");
  //Serial.println((int)echo_distance);
  return round(echo_distance);
}