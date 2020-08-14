  
// Function to read a text file one field at a time.
//
#include <SPI.h>
#include <SD.h>
#define CS_PIN 10
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
File file;

/*
 * Read a file one field at a time.
 *
 * file - File to read.
 *
 * str - Character array for the field.
 *
 * size - Size of str array.
 *
 * delim - String containing field delimiters.
 *
 * return - length of field including terminating delimiter.
 *
 * Note, the last character of str will not be a delimiter if
 * a read error occurs, the field is too long, or the file
 * does not end with a delimiter.  Consider this an error
 * if not at end-of-file.
 *
 */
size_t readField(File* file, char* str, size_t size, char* delim) {
  char ch;
  size_t n = 0;
  while ((n + 1) < size && file->read(&ch, 1) == 1) {
    // Delete CR.
    if (ch == '\r') {
      continue;
    }
    str[n++] = ch;
    if (strchr(delim, ch)) {
        break;
    }
  }
  str[n] = '\0';
  return n;
}
//------------------------------------------------------------------------------
#define errorHalt(msg) {Serial.println(F(msg)); while(1);}
//------------------------------------------------------------------------------
void setup() {
  Serial.begin(9600);

  
  // Initialize the SD.
  if (!SD.begin(CS_PIN)) errorHalt("begin failed");

  // Create or open the file.
  file = SD.open("alt-az-O482020.txt", FILE_WRITE);
  if (!file) errorHalt("open failed");

  // Rewind file so test data is not appended.
  file.seek(0);

  // Write test data.
//  file.print(F(
//    "field_1_1,field_1_2,field_1_3\r\n"
//    "field_2_1,field_2_2,field_2_3\r\n"
//    "field_3_1,field_3_2\r\n"           // missing a field
//    "field_4_1,field_4_2,field_4_3\r\n"
//    "field_5_1,field_5_2,field_5_3"     // no delimiter
//    ));

  // Rewind the file for read.
  file.seek(0);

  size_t n;      // Length of returned field with delimiter.
  char str[20];  // Must hold longest field with delimiter and zero byte.
  int count=0;  // to add the serial floats 
  float values[4]; //to make an array of 4 values
  
  // Read the file and print fields.
  while (true) {
    count = count + 1;
    n = readField(&file, str, sizeof(str), "\n- "); //added the - and a space too cause that is counted as a delimitor here

    // done if Error or at EOF.
    if (n == 0) break;

    // Print the type of delimiter.
    if (str[n-1] == '-' || str[n-1] == '\n' || str[n-1] == ' ') {
//      Serial.print(str[n-1] == ',' ? F("comma: ") : F("endl:  ")); not printing what it is
      
      // Remove the delimiter.
      str[n-1] = 0;
    } else {
      // At eof, too long, or read error.  Too long is error.
      Serial.print(file.available() ? F("error: ") : F("eof:   "));
    }
    // Print the field.
    Serial.println(str);

    if (count % 3 !=0){
      strf = (float) str //converting the string to float 
      cord[count]=strf; //the values keep on gettig added to the cord string
    }
  pinMode(encoderPin1, INPUT); 
  pinMode(encoderPin2, INPUT);

  digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin2, HIGH); //turn pullup resistor on

  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3) 
  attachInterrupt(0, updateEncoder, CHANGE); 
  attachInterrupt(1, updateEncoder, CHANGE);
  }
  

  // the expected output should be 
//  6:25:1
//  40.192... (the initial value of theta)
//  283.482... (the initial value of phi)
//  6:50:41
//  46.18300932842953  (the final value of theta)
//  286.7100693897322   (the final value of phi)
//  and the array will be the set of values
  
  file.close();
}
//------------------------------------------------------------------------------
void loop() {
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
  theta_1=cord[0];
  theta_2=cord[2];
  phi_1=cord[1];
  phi_2=cord[3];
  if (theta_1 - theta_2 >0)
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
