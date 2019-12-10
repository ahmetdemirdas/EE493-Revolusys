int databit;
int start=0;
int i=0;
int received_data[56];
int k = 0;
void setup() {
  // put your setup code here, to run once:
pinMode(10,INPUT);
Serial.begin(9600);
for(int a = 0; a < 56; a++)
{
  received_data[a]=0;
  
  }
}

void loop() {
  // put your main code here, to run repeatedly:
/*
while(i<57&& start==1)
{
  databit= digitalRead(10);
  delayMicroseconds(25);
  received_data[i] = databit;
  i++;   
  }

if(i == 57 )
{
    for( k = 0; k<56; k++);
    {
    Serial.println(received_data[k]);
    delay(100);
    }
  }  
*/
while(start==0)
{
  databit= digitalRead(10);
delayMicroseconds(50);
  
  if(databit==1)
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
     
     if(databit==1)
    {
     databit= digitalRead(10);
     delayMicroseconds(50);     
     
     if(databit == 1)
     {
      databit= digitalRead(10);
     delayMicroseconds(30);
     start=1;
     
     
     }
    }
    }
    }
  }
}
if(start)
{
  while(i<56)
  {
    databit= digitalRead(10);
     delayMicroseconds(50);
     received_data[i]= databit;
     i++;
    }
  }

  if(i==56)
  {
    i++;
    for(int ctr=0;ctr<56;ctr++)
      {
        Serial.print(received_data[ctr]);
        Serial.print(" ");
        
        
        }
    }

  
}
