#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Inițializează driverul PCA9685
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  Serial.begin(9600);
  Serial.println("Pornire PCA9685");
  
  pwm.begin();
  pwm.setPWMFreq(60); // Setare frecvență PWM pentru servouri (50Hz)
}

void loop() {

  int neutralHeight = 465, neutralPort = 276, neutralStarboard = 340;

  pwm.setPWM(1, 0, neutralHeight);
  delay(1000);

  // pwm.setPWM(2, 1, neutralPort);
  // delay(1000);

  // pwm.setPWM(3, 2, neutralStarboard);
  // delay(1000);
}
