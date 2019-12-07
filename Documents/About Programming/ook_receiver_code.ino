int databit;
int start=0;
int i=0;
int received_data[100];
int k = 0;
void setup() {
  // put your setup code here, to run once:
pinMode(10,INPUT);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
databit= digitalRead(10);
delayMicroseconds(50);
if(start == 1 && i<100)
{
  received_data[i] = databit;
  i++;
  
  
  }
  if(i == 100 && k<100)
  {
    for( k = 0; k<100; k++)
    Serial.println(received_data[k]);
    }

while(start==0)
{if(databit==1)
{
  databit= digitalRead(10);
  delayMicroseconds(50);
  if(databit==0)
  {
     databit= digitalRead(10);
     delayMicroseconds(50);
     if(databit==1)
    {
     databit= digitalRead(10);
     delayMicroseconds(50);
     if(databit==0)
    {
     databit= digitalRead(10);
     delayMicroseconds(50);     
     if(databit == 0)
     {
      databit= digitalRead(10);
     delayMicroseconds(50);
     start=1;
     }
    }
    }
    }
  }
}


{
  
  
  
  }


  

}
