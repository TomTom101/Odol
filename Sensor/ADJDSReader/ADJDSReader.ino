#include <ADJDS311.h>
#include <Calibration.h>
#include <Wire.h>

//#define DEBUG

int sensorLed_pin = 2; //LED on the ADJDS-311
ADJDS311 colorSensor(sensorLed_pin);

// These constants won't change:
const int sensorPin = A0;    // pin that the sensor is attached to
const int ledPin = 13;        // pin that the LED is attached to

const int avgValues = 5;
unsigned int sensorAvg[4][avgValues];

boolean use_stored_calibration = true;

Calibration cal = Calibration();

void setup() {
  pinMode(13, OUTPUT);

  Serial.begin(9600);
  /*
  Weisspunkt das an init uebergeben
   colorCap[0] = 9;
   colorCap[1] = 9;
   colorCap[2] = 2;
   colorCap[3] = 5;
   */
  colorSensor.init();
  //Calibrate white 
  //Need to hold white card in front (1-3mm) of it to calibrate from
  /*
  
   	colorCap[0] = 9;
   	colorCap[1] = 9;
   	colorCap[2] = 2;
   	colorCap[3] = 5;
   	// values must be between 0 and 15
   	colorInt[0] = 2048;
   	colorInt[1] = 2048;
   	colorInt[2] = 2048;
   	colorInt[3] = 2048;  
   Calibration settings
   color half:     1364
   clear half:     438
   red:     1
   green:     0
   blue:     0
   */

  if(use_stored_calibration) {
    cal.colorHalf = 150;
    cal.clearHalf = 100;
    cal.capacitor.red = 7;
    cal.capacitor.green = 5;
    cal.capacitor.blue = 0;

  } 
  else {
    colorSensor.ledOn(); //turn LED onS
  }

  cal = colorSensor.calibrate(cal);
  sendCalibrationData(cal);
  colorSensor.ledOff(); //turn LED on

#ifdef DEBUG
  Serial.print("color half: " );
  Serial.println(cal.colorHalf);  // This calibrates R, G, and B int registers
  Serial.print("clear half: " );
  Serial.println(cal.clearHalf);  // This calibrates the C int registers
  Serial.print("red: " );
  Serial.println(cal.capacitor.red);
  Serial.print("green: " );
  Serial.println(cal.capacitor.green);
  Serial.print("blue: ");
  Serial.println(cal.capacitor.blue);
#endif

}

void sendCalibrationData(Calibration cal) {
  Serial.write("c");
  Serial.write(getMultibyteFromInt(cal.colorHalf), 2);
  Serial.write(getMultibyteFromInt(cal.clearHalf), 2);
  Serial.write(cal.capacitor.red);
  Serial.write(cal.capacitor.green);
  Serial.write(cal.capacitor.blue);

}


void loop() {
  if(Serial.available()) {

    if(Serial.peek() == 115) { // "s" 
      Serial.read();
      digitalWrite(13, HIGH); 
      colorSensor.ledOn(); //turn LED onS
      Calibration cal = Calibration();
      cal = colorSensor.calibrate(cal);
      sendCalibrationData(cal);
      delay(500);
      colorSensor.ledOff(); //turn LED on

      digitalWrite(13, LOW);

    } 
    else {
      if(Serial.read() == 120) { // "x"  
        colorSensor.ledOn();
      }
    }
  }

  // read the sensor:
  RGBC color = colorSensor.read();

#ifndef DEBUG
  Serial.write("#");
  //    Serial.write(getMultibyteFromInt(getAvg(0, color.red)), 2);
  //    Serial.write(getMultibyteFromInt(getAvg(1, color.green)), 2);
  //    Serial.write(getMultibyteFromInt(getAvg(2, color.blue)), 2);
  //    Serial.write(getMultibyteFromInt(getAvg(3, color.clear)), 2);
  Serial.write(getMultibyteFromInt(color.red), 2);
  Serial.write(getMultibyteFromInt(color.green), 2);
  Serial.write(getMultibyteFromInt(color.blue), 2);
  Serial.write(getMultibyteFromInt(color.clear), 2);    
  // 4 individuelle writes ..., nicht ein int array
#endif

  delay(60000);
}

byte* getMultibyteFromInt(int i) {
  union {
    int  i;
    byte b[2];
  } 
  serial_byte;
  serial_byte.i = i;
  return serial_byte.b;

}

int getAvg(int index, int reading) {
  int avg = reading;
  for(int i=avgValues-1;i>0;i--) {
    sensorAvg[index][i] = sensorAvg[index][i-1];
    avg+=sensorAvg[index][i];
  }

  sensorAvg[index][0] = reading;

  return round(avg/avgValues);
}




