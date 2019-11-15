
// Author: Ian Kriner

//PIN DECLARATIONS//

int GPIO [16] = {A0,A1,2,3,4,5,6,A2,A3,7,8,9,10,11,12,13}; // sets up the IO ports to the device
int Sclk = 3;         //Serial Clock
int Rclk = 2;         //Register Clock
int Ser  = 4;         //Serial Data Out
int Clr  = 0;         //Clear

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//Variables//

bool Read [16];      //The state of the pins Read In
bool DIR  [16];      //Sets the direction of the IO pins 1 is output 0 is input
bool cnfgFlag = 0;   //Flag for if the config has been done or not
int r         = 0;   //the values read from the IO ports
int GPIO_NUM  = 16;  //the number of GPIO pins set up
int outputs;
//ERROR List//
String ERROR1 = "ERROR 1: GPIO have not been configured";
String ERROR2 = "ERROR 2: Missing Modifier";
String ERROR3 = "ERROR 3: Case not found";

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//Prototypes//
void shift(int sft);   //Writes to the SIPO Registers to control the relays
void cnfg(int a);      //Configures the Direction(input or output) of the GPIO
int readIO();         //Reads the Input pins only and Posts it to the serial port as a
                       //Decimal number which in binary corrisponeds to the state of each pin
void writeIO(int wrt); //Writes to the Output pins only send it a Decimal Number which in
                       //binary coresponds to the pins you want written High

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void setup() {
//  for(int x=0;x<16;x++) // sets all GPIO to the device to inputs they will be configured later
//  {
//    pinMode(GPIO[x],INPUT);
//  }

  pinMode(Ser,  OUTPUT); //Sets the control signals to outputs for the SIPO registers
  pinMode(Sclk, OUTPUT);
  pinMode(Rclk, OUTPUT);
  pinMode(Clr,  OUTPUT);

  shift(0);
  cnfg(27675);
  Serial.begin(115200);   // opens serial port, sets data rate to 9600 bps
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void loop()
{
  if (Serial.available() > 0)         //if serial data is available
  {
    switch(Serial.read())                        //decides what to do depending on first char
    {
      case '*':                       //relay case to write to the relays
        if(Serial.available() >0)     //Makes sure there is something else to read from the serial buffer
          shift(Serial.parseInt());   //parses an int from the serial buffer then sends it to shift
        else
          Serial.println(ERROR2);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case '^':                       //IO configuration case to set direction of IO
        if(Serial.available() >0)     //Makes sure there is something else to read from the serial buffer
        {
          cnfg(Serial.parseInt());    //parses an int from the serial buffer then sends it to cnfg to set io directions
        }
        else
          Serial.println(ERROR2);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case 'r':                       //Read pins if the config has been done
        if(cnfgFlag)                //If configuration has occured read the inputs else send error message
          Serial.println(readIO());
        else
          Serial.println(ERROR1);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case 'w':                       //Write to the output if the config has been done else send error message
        if(Serial.available()>0)
        {
          if(cnfgFlag)                //If configuration has occured write out the parsed int to the outputs
            writeIO(Serial.parseInt());
          else
          {
            Serial.println(ERROR1);
            Serial.parseInt();
          }
        }
        else
            Serial.println(ERROR2);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case 'c':                       //clears the configuration if another chip is being tested or anohther configurations is needed
        for(int u = 0; u<16;u++)      //Sets all GPIO to inputs and the direction back to 0
        {
          DIR[u]=0;
          pinMode(GPIO[u],INPUT);
        }
        cnfgFlag=0;                 //Resets the configFlag to prevent any reading or writing from GPIO
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case 's': //Single Relay Write uses the Relay number instead of a decimal codded binary number
        if(Serial.available()>0)
        {
          shift((1<<(Serial.parseInt()-1)));
        }
       else
          Serial.println(ERROR2);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case '@': //Pre-Configured Cases for certain ICs
        if(Serial.available()>0)
        {
          switch(Serial.parseInt())
          {
            case 1:  //Case for Ian's and Noahs IC
              cnfg(27675);
              break;
            case 2: //Case for Rice's IC
              cnfg(27675);
              break;
            default:
              break;
          }
        }
        else
          Serial.println(ERROR2);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case 't': //Write out special cases for all gates at the same time
        if(Serial.available()>0)
        {
          switch(Serial.parseInt())
          {
            case 0:
              writeIO(0);     //A and B is low
              break;
            case 1:
              writeIO(18450); //B is high A is low
              break;
            case 2:
              writeIO(9225);  //A is high B is low
              break;
            case 3:
              writeIO(27675); //A and B is high
              break;
            default:
              writeIO(0);
              break;
          }
        }
        else
          Serial.println(ERROR2);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      case 'o':
         if(cnfgFlag)                //Outputs a 4 bit number which is the state of the outputs
         {
          outputs=readIO();
          outputs=outputs&4644;
          if(outputs&0x1000)
            Serial.print('1');
          else
            Serial.print('0');
          if(outputs&0x200)
            Serial.print('1');
          else
            Serial.print('0');
          if(outputs&0x20)
            Serial.print('1');
          else
            Serial.print('0');
          if(outputs&0x4)
            Serial.print('1');
          else
            Serial.print(0);
          Serial.println();
         }
        else
          Serial.println(ERROR1);
        break;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      default:
          Serial.println(ERROR3);
        break;
      }
    }
  }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void shift(int sft) // DO NOT FUCK WITH THIS IT WORKS AND WONT IF YOU FUCK WITH IT
{
  digitalWrite(Rclk,0);
  //Sets Rclk to 0 to make sure the relays are not changed while writing to the registers
  digitalWrite(Clr,1);
  //Sets clear to high to allow for output
  for(int y = 15; y >=0; y--) //Loops thourgh all the bytes needed
  {
    digitalWrite(Sclk,0); //Sets Serial Clock Low
    if(sft & (1<<y))  //Masks the input number to find state of relay
      digitalWrite(Ser, 1); //Turns on that relay
    else
      digitalWrite(Ser, 0); //Turns off that relay
    digitalWrite(Sclk, 1);//Toggles serial clock to proceed to changing the state of the next relay
  }
  digitalWrite(Rclk, 1); //Toggles Rclk to move from the read registers to the relay registers
  Serial.println("done");
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void cnfg(int a)
{
  for(int x=0; x<GPIO_NUM;x++)
  {
    if(a & (1<<x))
    {
      pinMode(GPIO[x],OUTPUT); //sets the GPIO as an output
      DIR[x] = 1;              //1 equals output 0 input stores the setting into an array
    }
    else
     {
      pinMode(GPIO[x],INPUT);
      DIR[x] = 0;
     }
  }
  cnfgFlag=1;
  Serial.println("done");
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int readIO()
{
  r=0;                                  //r is the read values
  for(int t=0;t<16;t++)
  {
    if(!DIR[t]&&digitalRead(GPIO[t]))                         //if the GPIO is an input
      r|=1<<t;     //Reads the GPIO and stores it in its bitwise place in r
  }
  //Serial.println(r);                    //prints r to the serial port
  return(r);
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void writeIO(int wrt)
{
  for(int t=0;t<16;t++)
  {
    if(DIR[t])                      //if the GPIO is an Output
    {
      if(wrt & (1<<t))              //if the Output should be high
        digitalWrite(GPIO[t],1);    //writes high to the output
      else
        digitalWrite(GPIO[t],0);    //writes low to the output
    }
  }
  Serial.println("done");           //sends a done signal for writing IO
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
