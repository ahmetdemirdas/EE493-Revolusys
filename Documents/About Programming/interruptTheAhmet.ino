
int databit;
int start=0;
int i=0;
int received_data[150];
int k = 0;
unsigned long previousTime;
void setup() {
  // put your setup code here, to run once:
pinMode(3,INPUT);
Serial.begin(9600);
for(int a = 0; a <150; a++)
{
  received_data[a]=2;
  }
}



void loop() {
  // put your main code here, to run repeatedly:

while(start==0)
{
  databit= digitalRead(3);
  delayMicroseconds(100);
  if(databit==1)
  {
   databit= digitalRead(3);
  delayMicroseconds(100);
  //Serial.println("dod");
  if(databit==1)
  {
    databit= digitalRead(3);
  delayMicroseconds(100);
  if(databit==1)
{
  databit= digitalRead(3);
  delayMicroseconds(100);
  
  if(databit==1)
  {
     databit= digitalRead(3);
     delayMicroseconds(100);
     
     if(databit==1)
    {
     databit= digitalRead(3);
        
     delayMicroseconds(100);
     
     if(databit==0)
    {
     databit= digitalRead(3);
     attachInterrupt(1,riseedge,RISING);     
    }
    }
    }
  }
}
}
}

if(start)
{
while(i<150)
{ 
  if(i==0)
  {
     
    delayMicroseconds(99);
    databit = digitalRead(3);
    received_data[i] = databit;
    i++;
   
    }
    
  if(i>0)
  {
    
    delayMicroseconds(99);
    databit = digitalRead(3);
    received_data[i] = databit;
    i++; 
    
    if(i==50)
    {
      
      delayMicroseconds(100);
      databit = digitalRead(3);
      received_data[i] = databit;
      i++;
      
      
      }
    }
  
 
 /*  unsigned long currentTime = micros();
if(i<50 && start && (currentTime - previousTime > 50))
{
  databit = digitalRead(3);
  received_data[i] = databit;
  i++; 
  previousTime = currentTime;
 
  }*/
  
}
    
  if(i==150)
  {
    i++;
    for(int ctr=0;ctr<150;ctr++)
      {
        Serial.print(received_data[ctr]);
        Serial.print(" ");
        
        
        }
    }

}
}

void riseedge() 
{

  //delayMicroseconds(25);
/*unsigned long  interruptTime = micros();
  while(micros()<(50+interruptTime))
    {
      }*/
 //unsigned long currentTime = micros(); 

 start=1;
  detachInterrupt(3);
}
