/*
  Omny_wheel_motion.h - library for Osoyoo car motion command.
  Created by Olivier Georgeon, june 20 2021
  released into the public domain
*/
#include "Arduino.h"
#include "Wheel.h"
#include "Robot_define.h"

//#define speedPinR 9   //  RIGHT WHEEL PWM pin D45 connect front MODEL-X ENA
//#define RightMotorDirPin1  22    //Front Right Motor direction pin 1 to Front MODEL-X IN1  (K1)
//#define RightMotorDirPin2  24   //Front Right Motor direction pin 2 to Front MODEL-X IN2   (K1)
//#define LeftMotorDirPin1  26    //Left front Motor direction pin 1 to Front MODEL-X IN3 (  K3)
//#define LeftMotorDirPin2  28   //Left front Motor direction pin 2 to Front MODEL-X IN4 (  K3)
//#define speedPinL 10   // Left WHEEL PWM pin D7 connect front MODEL-X ENB
//
//#define speedPinRB 11   //  RIGHT WHEEL PWM pin connect Back MODEL-X ENA
//#define RightMotorDirPin1B  5    //Rear Right Motor direction pin 1 to Back MODEL-X IN1 (  K1)
//#define RightMotorDirPin2B 6    //Rear Right Motor direction pin 2 to Back MODEL-X IN2 (  K1)
//#define LeftMotorDirPin1B 7    //Rear left Motor direction pin 1 to Back MODEL-X IN3  K3
//#define LeftMotorDirPin2B 8  //Rear left Motor direction pin 2 to Back MODEL-X IN4  k3
//#define speedPinLB 12    //   LEFT WHEEL  PWM pin D8 connect Rear MODEL-X ENB
//
Wheel::Wheel()
{
}
void Wheel::setup()
{
  //Pins initialize
  pinMode(RightMotorDirPin1, OUTPUT);
  pinMode(RightMotorDirPin2, OUTPUT);
  pinMode(speedPinL, OUTPUT);

  pinMode(LeftMotorDirPin1, OUTPUT);
  pinMode(LeftMotorDirPin2, OUTPUT);
  pinMode(speedPinR, OUTPUT);

  pinMode(RightMotorDirPin1B, OUTPUT);
  pinMode(RightMotorDirPin2B, OUTPUT);
  pinMode(speedPinLB, OUTPUT);

  pinMode(LeftMotorDirPin1B, OUTPUT);
  pinMode(LeftMotorDirPin2B, OUTPUT);
  pinMode(speedPinRB, OUTPUT);

  stopMotion();
}

void Wheel::turnInSpotLeft(int speed)
{
  setMotion(-speed, -speed, speed, speed);
}
void Wheel::goBack(int speed)
{
  setMotion(-speed, -speed, -speed, -speed);
}
void Wheel::turnInSpotRight(int speed)
{
  setMotion(speed, speed, -speed, -speed);
}
void Wheel::turnFrontLeft(int speed)
{
  setMotion(speed / 2, -speed, speed, speed / 2);
}
void Wheel::turnFrontRight(int speed)
{
  setMotion(speed / 2, speed, -speed, speed / 2);
}
void Wheel::shiftLeft(int speed)
{
  setMotion( -speed, speed, -speed, speed);
}
void Wheel::shiftRight(int speed)
{
  setMotion(speed, -speed, speed, -speed);
}
void Wheel::turnLeft(int speed)
{
  setMotion( 0, speed, 0, speed);
  //setMotion(0, 0, speed, speed);
}
void Wheel::goForward(int speed)
{
  setMotion(speed, speed, speed, speed);
}
void Wheel::turnRight(int speed)
{
  setMotion(speed, 0, speed, 0);
  //setMotion(speed, speed, 0, 0);
}

void Wheel::setMotion(int speed_fl, int speed_rl, int speed_rr, int speed_fr){
  frontLeftWheel(speed_fl);
  rearLeftWheel(speed_rl);
  frontRightWheel(speed_fr);
  rearRightWheel(speed_rr);
}

void Wheel::stopMotion()    //Stop
{
  analogWrite(speedPinLB,0);
  analogWrite(speedPinRB,0);
  analogWrite(speedPinL,0);
  analogWrite(speedPinR,0);
}

/*motor control*/
void Wheel::frontRightWheel(int speed)
{
  if (speed > 0) {
    // Forward
    digitalWrite(RightMotorDirPin1,LOW);
    digitalWrite(RightMotorDirPin2,HIGH);
    analogWrite(speedPinR,speed * ROBOT_FRONT_RIGHT_WHEEL_COEF);
  } else {
    // Backward
    digitalWrite(RightMotorDirPin1,HIGH);
    digitalWrite(RightMotorDirPin2,LOW);
    analogWrite(speedPinR,-speed * ROBOT_FRONT_RIGHT_WHEEL_COEF);
  }
}
void Wheel::frontLeftWheel(int speed)
{
  if (speed > 0) {
    // Forward
    digitalWrite(LeftMotorDirPin1,LOW);
    digitalWrite(LeftMotorDirPin2,HIGH);
    analogWrite(speedPinL,speed * ROBOT_FRONT_LEFT_WHEEL_COEF);
  } else {
    // Backward
    digitalWrite(LeftMotorDirPin1,HIGH);
    digitalWrite(LeftMotorDirPin2,LOW);
    analogWrite(speedPinL,-speed * ROBOT_FRONT_LEFT_WHEEL_COEF);
  }
}
void Wheel::rearRightWheel(int speed)
{
  if (speed > 0) {
    // Forward
    digitalWrite(RightMotorDirPin1B, LOW);
    digitalWrite(RightMotorDirPin2B,HIGH);
    analogWrite(speedPinRB,speed * ROBOT_REAR_RIGHT_WHEEL_COEF); // corrective coefficient depends on robot
  } else {
    // Backward
    digitalWrite(RightMotorDirPin1B, HIGH);
    digitalWrite(RightMotorDirPin2B,LOW);
    analogWrite(speedPinRB,-speed * ROBOT_REAR_RIGHT_WHEEL_COEF); // corrective coefficient depends on robot
  }
}
void Wheel::rearLeftWheel(int speed)
{
  if (speed > 0) {
    // Forward
    digitalWrite(LeftMotorDirPin1B,LOW);
    digitalWrite(LeftMotorDirPin2B,HIGH);
    analogWrite(speedPinLB,speed * ROBOT_REAR_LEFT_WHEEL_COEF); // corrective coefficient depends on robot
  } else {
    // Backward
    digitalWrite(LeftMotorDirPin1B,HIGH);
    digitalWrite(LeftMotorDirPin2B,LOW);
    analogWrite(speedPinLB,-speed * ROBOT_REAR_LEFT_WHEEL_COEF); // corrective coefficient depends on robot
  }
}

