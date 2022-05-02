#define ROBOT_ID 2 // 0: regular Osoyoo robot, 1: robot BSN, 2: robot Olivier, 3: robot SHS, 4: robot SHS with GY86

#define ROBOT_HEAD_X 80  // X position of the head

#if ROBOT_ID == 1

#warning "Compiling for BSN's robot"
#define ROBOT_HAS_MPU6050  true
#define ROBOT_HAS_HMC5883L false
#define ROBOT_REAR_RIGHT_WHEEL_COEF 1
#define ROBOT_REAR_LEFT_WHEEL_COEF 1.2
#define ROBOT_FRONT_RIGHT_WHEEL_COEF 1
#define ROBOT_FRONT_LEFT_WHEEL_COEF 1
#define TURN_SPOT_MAX_DURATION 2400
#define TURN_SPOT_ENDING_DELAY 500
#define TURN_SPOT_ENDING_ANGLE 15
#define ACCELERATION_X_OFFSET -40
#define ACCELERATION_SHOCK_THRESHOLD -200
#define ACCELERATION_BLOCK_THRESHOLD 60  // TODO depends whether the interaction starts when the robot is immobile
#define GYRO_COEF 1 // IMU is upright
#define GYRO_SHOCK_THRESHOLD 1 // °/s
#define ROBOT_SERVO_PIN 4  // 13 Changed because 13 is used for internal led

#elif ROBOT_ID == 2

#warning "Compiling for Olivier's robot"
#define ROBOT_HAS_MPU6050  true
#define ROBOT_HAS_HMC5883L true
#define ROBOT_REAR_RIGHT_WHEEL_COEF 1.1
#define ROBOT_REAR_LEFT_WHEEL_COEF 1
#define ROBOT_FRONT_RIGHT_WHEEL_COEF 1
#define ROBOT_FRONT_LEFT_WHEEL_COEF 1
#define TURN_SPOT_MAX_DURATION 2400
#define TURN_SPOT_ENDING_DELAY 200
#define TURN_SPOT_ENDING_ANGLE 3
#define COMPASS_X_OFFSET 1475
#define COMPASS_Y_OFFSET -1685
#define ACCELERATION_X_OFFSET 550 //
#define ACCELERATION_SHOCK_THRESHOLD -400 // Below the threshold it is a strong deceleration = shock
#define ACCELERATION_BLOCK_THRESHOLD 60 // Below the threshold, the robot is blocked
#define GYRO_COEF 1 // UMI is upright
#define GYRO_SHOCK_THRESHOLD 1.5 // °/s Above the threshold is a shock to the left
#define ROBOT_SERVO_PIN 4

#elif ROBOT_ID == 3

#warning "Compiling for SHS's robot with GY521"
#define ROBOT_HAS_MPU6050  true
#define ROBOT_HAS_HMC5883L false
#define ROBOT_REAR_RIGHT_WHEEL_COEF 1
#define ROBOT_REAR_LEFT_WHEEL_COEF 1
#define ROBOT_FRONT_RIGHT_WHEEL_COEF 1
#define ROBOT_FRONT_LEFT_WHEEL_COEF 1.3
#define TURN_SPOT_MAX_DURATION 2400
#define TURN_SPOT_ENDING_DELAY 200
#define TURN_SPOT_ENDING_ANGLE 3
#define ACCELERATION_X_OFFSET 0 // TODO tune this value
#define ACCELERATION_SHOCK_THRESHOLD -200 // TODO set this value
#define ACCELERATION_BLOCK_THRESHOLD 30 // TODO set this value
#define GYRO_COEF -1 // IMU GY521 upside down
#define GYRO_SHOCK_THRESHOLD 1 // °/s TODO set this value
#define ROBOT_SERVO_PIN 4

#elif ROBOT_ID == 4

#warning "Compiling for SHS's robot with GY-86"
#define ROBOT_HAS_MPU6050  true
#define ROBOT_HAS_HMC5883L true
#define ROBOT_REAR_RIGHT_WHEEL_COEF 1
#define ROBOT_REAR_LEFT_WHEEL_COEF 1
#define ROBOT_FRONT_RIGHT_WHEEL_COEF 1
#define ROBOT_FRONT_LEFT_WHEEL_COEF 1.3
#define TURN_SPOT_MAX_DURATION 2400
#define TURN_SPOT_ENDING_DELAY 200
#define TURN_SPOT_ENDING_ANGLE 3
#define COMPASS_X_OFFSET 1020
#define COMPASS_Y_OFFSET -1300
#define ACCELERATION_X_OFFSET 35
#define ACCELERATION_SHOCK_THRESHOLD -200 // TODO set this value
#define ACCELERATION_BLOCK_THRESHOLD 30 // TODO set this value
#define GYRO_COEF 1
#define GYRO_SHOCK_THRESHOLD 1 // °/s TODO set this value
#define ROBOT_SERVO_PIN 4

#else

#warning "Compiling for a regular Osoyoo robot"
#define ROBOT_HAS_MPU6050  false
#define ROBOT_HAS_HMC5883L false
#define ROBOT_REAR_RIGHT_WHEEL_COEF 1
#define ROBOT_REAR_LEFT_WHEEL_COEF 1
#define ROBOT_FRONT_RIGHT_WHEEL_COEF 1
#define ROBOT_FRONT_LEFT_WHEEL_COEF 1
#define TURN_SPOT_MAX_DURATION 1300
#define TURN_SPOT_ENDING_DELAY 200
#define TURN_SPOT_ENDING_ANGLE 3
#define ROBOT_SERVO_PIN 13

#endif
