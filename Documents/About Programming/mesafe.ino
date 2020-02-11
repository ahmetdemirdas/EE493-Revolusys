int trigPin = 2; 
int echoPin = 7; 

long sure;
long uzaklik;

void setup(){
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin,INPUT); 
  Serial.begin(9600); 
}
void loop()
{
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);   
  sure = pulseIn(echoPin, HIGH); 
  uzaklik= sure /29.1/2;             
  if(uzaklik > 200)
    uzaklik = 200;
  Serial.print("Uzaklik ");  
  Serial.print(uzaklik); 
  Serial.println(" CM ");  
  delay(100); 
}
