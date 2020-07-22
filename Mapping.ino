#include <Stepper.h>
const int stepsPerRevolution = 200;
Stepper myStepper1(stepsPerRevolution, 8, 9, 10, 11);//azimuth
Stepper myStepper2(stepsPerRevolution, 2, 3, 4, 5);//altitude
int stepcount=0;
char inp;
float theta_1;
float theta_2;
float phi_1;
float phi_2;
float theta_present= 0;
float phi_present= 0;
int r=0.1;

//these pins can not be changed 2/3 are special pins
int encoderPin1 = 2;
int encoderPin2 = 3;

long int mapped;

volatile int lastEncoded = 0;
volatile long encoderValue = 0;

long lastencoderValue = 0;

int lastMSB = 0;
int lastLSB = 0;

void setup() {
  Serial.begin (9600);

  pinMode(encoderPin1, INPUT); 
  pinMode(encoderPin2, INPUT);

  digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin2, HIGH); //turn pullup resistor on

  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3) 
  attachInterrupt(0, updateEncoder, CHANGE); 
  attachInterrupt(1, updateEncoder, CHANGE);

}

void loop(){ 
  //Do stuff here
  mapped=map(encoderValue, 0, 600, 0, 360);
  //Serial.println(encoderValue);
 // delay(1000); //just here to slow down the output, and show it will work  even during a delay
if(mapped<=.05*theta2)
  {backlash();}
}


void backlash()
  {if(Serial.available())
  {
  theta_1=Serial.read();
  theta_2=Serial.read();
  phi_1=Serial.read();
  phi_2=Serial.read();
  if (theta_1 -theta_2 >0)
  { 
    float a;
    a=theta_1;
    theta_1=theta_2;
    theta_2=a;
  }
  myStepper1.step(ceil(theta_1/r));
  myStepper2.step(ceil(phi_1/r));
  for (int i = 0; i<=ceil((phi_1-phi_2)/(2*r)); i++)
  {
    for( i =0;i<=ceil((theta_2-theta_1)/r);i++)
    {
      myStepper1.step(1);
      theta_present = theta_present +r;
      if(theta_present-mapped<-0.05)
      {
        myStepper1.step(-1);
      }
      else if(theta_present-mapped>0.05)
      {
        myStepper1.step(1);
      }
    }
    if(phi_1 - phi_2 < 0)
    {
      myStepper2.step(1);
      phi_present =phi_present +r;
      
    }
    else
    {
      myStepper2.step(-1);
      phi_present =phi_present -r;
    }
    for( i =0;i<=ceil((theta_2-theta_1)/r);i++)
    {
      myStepper1.step(-1);
      theta_present = theta_present - r;
      if(theta_present-mapped<-0.05)
      {
        myStepper1.step(1);
      }
      else if(theta_present-mapped>0.05)
      {
        myStepper1.step(-1);
      }
    }
    if(phi_1 - phi_2 < 0)
    {
      myStepper2.step(-1);
      phi_present = phi_present -r;
    }
    else
    {
      myStepper2.step(1);
      phi_present = phi_present +r;
    }
  }
  }
    }


void updateEncoder(){
  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue ++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue --;

  lastEncoded = encoded; //store this value for next time
}
