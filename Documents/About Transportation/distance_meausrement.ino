/*
 * created by Rui Santos, https://randomnerdtutorials.com
 * 
 * Complete Guide for Ultrasonic Sensor HC-SR04
 *
    Ultrasonic sensor Pins:
        VCC: +5VDC
        Trig : Trigger (INPUT) - Pin11
        Echo: Echo (OUTPUT) - Pin 12
        GND: GND
 */
 
int trigPin = 8;    // Trigger
int echoPin = 9;    // Echo
int counter = 0;
float number=0;
float duration, cm, inches;
float mean;
float arrayA[50];
 
void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}
 
void loop() {
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  while(counter <  50)
  {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
 
  // Convert the time into a distance
  cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  inches = (duration/2) / 74;   // Divide by 74 or multiply by 0.0135
  
  arrayA[counter] = cm;
  Serial.print(cm);

  Serial.println();
  number= number + cm;

  
  delay(250);
  counter ++;

  };
  if(counter == 50)
  {
    number = number/50;

    float sqDevSum = 0.0;

  for(int i = 0; i < 50; i++) {
    // pow(x, 2) is x squared.
    sqDevSum += pow((number - float(arrayA[i])), 2);
  }

  // STEP 3, FIND THE MEAN OF THAT
  // STEP 4, TAKE THE SQUARE ROOT OF THAT

  float stDev = sqrt(sqDevSum/50);
    Serial.print("average: ");
    Serial.println(number);
    Serial.print("standard dev:");
    Serial.println(stDev);
  };
  counter = 51;
}
