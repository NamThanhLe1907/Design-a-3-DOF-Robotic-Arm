#include <AccelStepper.h>

#define ENABLE_PIN 8
#define MOTOR1_STEP_PIN 2
#define MOTOR1_DIR_PIN 3
#define MOTOR2_STEP_PIN 4
#define MOTOR2_DIR_PIN 5
#define MOTOR3_STEP_PIN 6
#define MOTOR3_DIR_PIN 7
#define hut 9

const int stepsPerRevolution = 200;
const int speed = 3000;
int FKne = 0;
int IKne = 0;
int Stop_mode = 0;
int Start_mode = 0;

AccelStepper stepper1(AccelStepper::DRIVER, MOTOR1_STEP_PIN, MOTOR1_DIR_PIN);
AccelStepper stepper2(AccelStepper::DRIVER, MOTOR2_STEP_PIN, MOTOR2_DIR_PIN);
AccelStepper stepper3(AccelStepper::DRIVER, MOTOR3_STEP_PIN, MOTOR3_DIR_PIN);

int angleToSteps(int angle) {
  int steps = ((angle / 360.0 * (stepsPerRevolution+40) * 32)/20 *60);
  return steps;
}

void setup() {
  Serial.begin(9600);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(hut, OUTPUT);
  stepper1.setMaxSpeed(speed);
  stepper1.setAcceleration(speed);
  stepper2.setMaxSpeed(speed);
  stepper2.setAcceleration(speed);
  stepper3.setMaxSpeed(speed);
  stepper3.setAcceleration(speed);
  digitalWrite(ENABLE_PIN, 1);
  digitalWrite(hut,LOW);
}

void loop() {
  Operation(); // Xử lý các lệnh từ Python
  if (FKne == 1) {
    FK();
  }
  if (IKne == 1) {
    IK();
  }
  // Kiểm tra xem các động cơ có cần di chuyển không và di chuyển tuần tự từng động cơ
  if (stepper1.distanceToGo() != 0) {
    stepper1.run();
  } else if (stepper2.distanceToGo() != 0) {
    stepper2.run();
  } else if (stepper3.distanceToGo() != 0) {
    stepper3.run();
  }
}

void FK() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    FKne = 1; // Đặt biến FKne thành 1
    IKne = 0; // Reset biến IKne
    
    int start1 = command.indexOf('(') + 1;
    int end1 = command.indexOf(')');
    int angle1 = command.substring(start1, end1).toInt();

    int start2 = command.indexOf('(', end1) + 1;
    int end2 = command.indexOf(')', start2);
    int angle2 = command.substring(start2, end2).toInt();

    int start3 = command.indexOf('(', end2) + 1;
    int end3 = command.indexOf(')', start3);
    int angle3 = command.substring(start3, end3).toInt();

    if (command.startsWith("-")) {
      angle1 *= -1;
      angle2 *= -1;
      angle3 *= -1;
    }

    int steps1 = angleToSteps(angle1);
    int steps2 = angleToSteps(angle2);
    int steps3 = angleToSteps(angle3);

    // Quay từng động cơ một
    moveStepper(stepper1, steps1);
    moveStepper(stepper2, steps2);
    moveStepper(stepper3, steps3);
  }
}


void IK() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    // Kiểm tra xem lệnh có bắt đầu bằng "IK" hay không
    if (command.startsWith("IK")) {
      FKne = 0; // Reset biến FKne
      IKne = 1; // Đặt biến IKne thành 1

      int start1 = command.indexOf('(') + 1;
      int end1 = command.indexOf(')');
      int angle1 = command.substring(start1, end1).toInt();

      int start2 = command.indexOf('(', end1) + 1;
      int end2 = command.indexOf(')', start2);
      int angle2 = command.substring(start2, end2).toInt();

      int start3 = command.indexOf('(', end2) + 1;
      int end3 = command.indexOf(')', start3);
      int angle3 = command.substring(start3, end3).toInt();

      if (command[start1 - 1] == '-') {
        angle1 *= -1;
        angle2 *= -1;
        angle3 *= -1;
      }

      int steps1 = angleToSteps(angle1);
      int steps2 = angleToSteps(angle2);
      int steps3 = angleToSteps(angle3);

      // Quay từng động cơ một
      moveStepper(stepper1, steps1);
      moveStepper(stepper2, steps2);
      moveStepper(stepper3, steps3);
    }
  }
}


void Operation() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command.startsWith("S")) {
      digitalWrite(ENABLE_PIN, 0);
      digitalWrite(MOTOR1_DIR_PIN, 0);
      digitalWrite(MOTOR2_DIR_PIN, 0);
      digitalWrite(MOTOR3_DIR_PIN, 0);
      FKne = 0;
      IKne = 0;
      Serial.println("Robot mode: ON");
      Start_mode++;
      Stop_mode = 0;
    }
    else if (command.startsWith("RS")) {
      int angle1 = 0;
      int angle2 = 0;
      int angle3 = 0;

      int steps1 = angleToSteps(angle1);
      int steps2 = angleToSteps(angle2);
      int steps3 = angleToSteps(angle3);

      // Quay từng động cơ một
      moveStepper(stepper1, steps1);
      moveStepper(stepper2, steps2);
      moveStepper(stepper3, steps3);
    }
    else if (command.startsWith("E")) {
      digitalWrite(ENABLE_PIN, 1);
      Serial.println("Robot mode: OFF");
      Start_mode = 0;
      Stop_mode++;
      digitalWrite(MOTOR1_DIR_PIN, 0);
      digitalWrite(MOTOR2_DIR_PIN, 0);
      digitalWrite(MOTOR3_DIR_PIN, 0);
      FKne = 0;
      IKne = 0;
    }
    else if (command.startsWith("FK")) {
      FKne = 1;
      IKne = 0;
      command = "";
    }
    else if (command.startsWith("IK")) {
      FKne = 0;
      IKne = 1;
      command = "";
    }
    else if(command.startsWith("H")){
      FKne = 0;
      IKne = 0;
      digitalWrite(hut,LOW);
      command = "";
    }
    else if(command.startsWith("T")){
      FKne = 0;
      IKne = 0;
      digitalWrite(hut,HIGH);
      command = "";
    }
  }
}

// Hàm di chuyển động cơ với số bước nhất định và đợi cho đến khi hoàn thành
void moveStepper(AccelStepper &stepper, int steps) {
  stepper.moveTo(steps);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
}
