const int in1 = 10;         // Driver input pins
const int in2 = 11;         // Driver input pins
const int in3 = 12;         // Driver input pins
const int in4 = 13;         // Driver input pins
const int trigPin_1 = 2;    // Trigger forward
const int echoPin_1 = 3 ;    // Echo forward
const int trigPin_2 = 8;    // Trigger back
const int echoPin_2 = 9;    // Echo back
long dist;

void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(trigPin_1, OUTPUT);
  pinMode(echoPin_1, INPUT);
  pinMode(trigPin_2, OUTPUT);
  pinMode(echoPin_2, INPUT);
}

void loop() {
  dist = measure(trigPin_1, echoPin_1);
  while (dist > 15) {
    forward();
    dist = measure(trigPin_1, echoPin_1);
  } 
  brake();
  delay(600);

  dist = measure(trigPin_2, echoPin_2);
  while (dist > 15) {
    back();
    dist = measure(trigPin_2, echoPin_2);
  } 
  brake();
  delay(600);
}

long measure(int pinTrig, int pinEcho) {
  long duration, distance;
  
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
 
  duration = pulseIn(pinEcho, HIGH);
  distance = duration/59.2;
  delay(50);

  return distance;
}

void forward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);  
}

void back() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);  
}

void brake() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, HIGH);
}
