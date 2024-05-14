#include <IBusBM.h>

IBusBM ibusRc;

HardwareSerial& ibusRcSerial = Serial1;
HardwareSerial& debugSerial = Serial;

const int R_is = 2;
const int R_en = 3;
const int R_pmw = 4;
const int L_is = 5;
const int L_en = 6;
const int L_pmw = 7;
const int R_is1 = 8;
const int R_en1 = 22;
const int R_pmw1 = 10;
const int L_is1 = 11;
const int L_en1 = 12;
const int L_pmw1 = 13;
int leftenable = 0;
int rightenable = 0;
int forwardenable = 0;
int backwardenable = 0;
int speed = 0;

const int motor = 9;
int ch1 = 0;
int ch2 = 0;
int ch3 = 0;
int ch4 = 0;
int ch5 = 0;
int ch6 = 0;
int ch7 = 0;
int ch8 = 0;  

void setup() {
  // put your setup code here, to run once:
  debugSerial.begin(74880);
  ibusRc.begin(ibusRcSerial);


  pinMode(R_is, OUTPUT);
  pinMode(R_en, OUTPUT);
  pinMode(R_pmw, OUTPUT);
  pinMode(L_is, OUTPUT);
  pinMode(L_en, OUTPUT);
  pinMode(L_pmw, OUTPUT);

  pinMode(R_is1, OUTPUT);
  pinMode(R_en1, OUTPUT);
  pinMode(R_pmw1, OUTPUT);
  pinMode(L_is1, OUTPUT);
  pinMode(L_en1, OUTPUT);
  pinMode(L_pmw1, OUTPUT);

  pinMode(motor, INPUT);
  digitalWrite(R_is, 0);
  digitalWrite(L_is, 0);
  digitalWrite(R_en, 1);
  digitalWrite(L_en, 1);

  digitalWrite(R_is1, 0);
  digitalWrite(L_is1, 0);
  digitalWrite(R_en1, 1);
  digitalWrite(L_en1, 1);

  delay(2000) // wait for reciever to activate
}


// Read the number of a given channel and convert to the range provided.
// If the channel is off, return the default value
int readChannel(byte channelInput, int minLimit, int maxLimit, int defaultValue) {
  uint16_t ch = ibusRc.readChannel(channelInput);
  if (ch < 100) return defaultValue;
  return map(ch, 1000, 2000, minLimit, maxLimit);
}
  
void loop() {
  // put your main code here, to run repeatedly:
  int failsafe = 0;
  for (byte i = 0; i < 7; i++) {
    int value = readChannel(i, -100, 100, 0);
    debugSerial.print("Ch");
    debugSerial.print(i + 1);
    debugSerial.print(": ");
    debugSerial.print(value);
    debugSerial.print(" ");
    //channel 1 left and right
    if (i == 0) {
      ch1 = value;
    }
    //channel 2 fwd and bwd
    if (i == 1) {
      ch2 = value;
    }
    //channel 4 speed control
    if (i == 2) {
      ch3 = value;
    }
    if (i == 4) {
      ch5 = value;
    }
    if (i == 8) {
      ch6 = value;
    }
  }
  
  
  debugSerial.println();
  delay(5);

  speed = constrain(map(ch3, 0, 100, 0, 255), 0, 240);
  //on or enable switch
  if (ch5 == 100) {
    digitalWrite(R_en, 1);
    digitalWrite(L_en, 1);
    digitalWrite(R_en1, 1);
    digitalWrite(L_en1, 1);

    //weapon motor
    analogWrite(motor, map(ch6, 0, 100, 0, 255));
    if (ch1 > 40 && (ch2 > 40 || ch2 < -40)) {
      speed = constrain(map(ch3, 0, 100, 0, 255), 0, 240);
      //turn right fwd
      analogWrite(R_pmw, 0);
      analogWrite(L_pmw, speed);
      //left motor
      analogWrite(R_pmw1, speed);
      analogWrite(L_pmw1, 0);
    }
    if (ch1 < -40 && (ch2 > 40 || ch2 < -40)) {
      speed = constrain(map(ch3, 0, 100, 0, 255), 0, 240);
      //turn left fwd
      analogWrite(R_pmw, speed);
      analogWrite(L_pmw, 0);
      //left motor
      analogWrite(R_pmw1, 0);
      analogWrite(L_pmw1, speed);
    }

    if (ch1 > -20 && ch1 < 20 && ch2 < 0) {
      speed = constrain(map(ch3, 0, 100, 0, 255), 0, 240);
      //backward
      analogWrite(R_pmw, 0);
      analogWrite(L_pmw, speed);
      //left motor
      analogWrite(R_pmw1, 0);
      analogWrite(L_pmw1, speed);
    }
    if (ch1 > -20 && ch1 < 20 && ch2 > 0) {
      speed = constrain(map(ch3, 0, 100, 0, 255), 0, 240);
      //forward
      analogWrite(R_pmw, speed);
      analogWrite(L_pmw, 0);
      //left motor
      analogWrite(R_pmw1, speed);
      analogWrite(L_pmw1, 0);

    }
  }
  else {
    digitalWrite(R_en, 0);
    digitalWrite(L_en, 0);

    //weapon motor stopped
    analogWrite(motor,0);
    
    digitalWrite(R_en1, 0);
    digitalWrite(L_en1, 0);
  }
}
