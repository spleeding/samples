/**** Studio Jenna Sutela - HEADS FRIEZE / BREMEN  ****/

// BREMEN HEAD : Towards Mu
// FRIEZE HEAD 1 : Towards Gamma
// FRIEZE HEAD 2 : Towards Delta

// BASE PROGRAM:
// BOARD: CLASSIC

// Difference between Classic and Express - 
// Regarding Pin: On the Classic boards we use the NUMBER on the board
// Regarding Pin: On the Express we use the AX on the board

// Ardino Libraries
#include <Adafruit_CircuitPlayground.h>
#include <Arduino.h>


// WE USE THE EQUATION ((1/X Hz) * 1000)/2 
// TO GET THE PERIOD THE LIGHT HAS TO BE ON AND OFF IN EACH LOOP CYCLE 


/********* GLOBAL CONSTANTS AND VARIABLES ******************/

// CONSTANTS / MACROS

// We need a loop for the current to flow properly.

// NeoPixel Properties
#define NEO_PIX_PIN 6
#define NUM_NEO_PIX 24

#define STATETIME 30000 // 2 seconds - Change this in the program for the heads so that it stays for 30 secs or even more at a given freq before chaning.
#define CHANGEDIVIDER 60

// ARRAYS

// STATES - Gamma 12MS | 40Hz - Beta 20MS | 25Hz - Mu 38.46MS | 13Hz - Alpha 41.66MS | 12Hz - Theta 100MS | 5Hz - Delta 250MS | 2Hz or 125MS | 4Hz 
// 
float StateFrequencies[6] = {12.5, 20, 38.46, 41.66, 100, 250}; // Frequencies translated into ms for the delay function according to the above listing.

int GammaDist[6] = {65, 20, 10, 5, 0, 0};
int BetaDist[6] = {55, 25, 10, 5, 5, 0};
int MuDist[6] = {45, 20, 15, 10, 5, 5};
int AlphaDist[6] = {35, 15, 20, 10, 10, 10};
int ThetaDist[6] = {30, 10, 15, 15, 20, 10};
int DeltaDist[6] = {25, 10, 15, 15, 20, 15};


int Weigh(int StateWeights[6]) {
  // Declaring Index
  int Index = 0;
  // Summing up State Weights
  int SumOfWeights = 0;
  for (int i = 0; i < 6; i++){
    SumOfWeights += StateWeights[i];
  }
  // Weighted random selection
  int r = random(SumOfWeights);
  for (int j = 0; j < 6; j++) {
    if (r < StateWeights[j]) {
      Index = j;
      break;
    }
    r -= StateWeights[j];
  }
  return Index; 
}


// GLOBAL VARIABLES

// Initialize the Random Walk
int InitialIndex = 3; // Initalized from Mu
int StateIndex = InitialIndex;
float Freq = StateFrequencies[StateIndex];
float DeltaFreq = Freq;

int D = 0; // Gradual change counter.

// Timehandling 
unsigned long DeltaTime = 0;
unsigned long TimeCheck = 0;
bool Clocked = false; //Determining if a State has been entered.

// NeoPixel Ring
Adafruit_CPlay_NeoPixel ring = (NUM_NEO_PIX, NEO_PIX_PIN, NEO_GRB + NEO_KHZ800);


/**************************** SET UP **************************/

void setup() {
  
  Serial.begin(9600);

  // SET On Board NEO-PIXELS
  CircuitPlayground.begin(255); //Begins on max brightness (255)
  CircuitPlayground.clearPixels();

  // Pixel Ring:
  ring.begin(); // Begins on max brightness (255)

}


/*************************** MAIN LOOP *************************/

void loop() {
  

  // Get next State according to the probability distribution of the current state

  // Markov Chain Transitions
  switch (StateIndex) {
    
    case 0: // Gamma
    if (!Clocked) {
      Clocked = true; //Stamping in
      // Timing
      TimeCheck = millis();
      DeltaTime = 0;
      DeltaFreq = Freq;
      D = 0;
      Serial.println("STATE = Gamma");
    }
    // Gradual change from one state into the next.
    if (D < CHANGEDIVIDER) {
      Freq = Freq + ((StateFrequencies[StateIndex] - DeltaFreq)/CHANGEDIVIDER);
      // Serial.println(Freq);
      D++;
    }
    DeltaTime = millis() - TimeCheck;
    // std::cout << "DeltaTime = " << DeltaTime << std::endl;
    if (DeltaTime > STATETIME) {
      // Determining Next State
      StateIndex = Weigh(GammaDist);
      Clocked = false; // Stamping out
      DeltaTime = 0;
    }
    break;


    case 1: // Beta
    if (!Clocked) {
      Clocked = true;
      // Timing
      TimeCheck = millis();
      DeltaTime = 0;
      DeltaFreq = Freq;
      D = 0;
      Serial.println("STATE = Beta");
    }
    // Gradual change from on state into another
    if (D < CHANGEDIVIDER) {
      Freq = Freq + ((StateFrequencies[StateIndex] - DeltaFreq)/CHANGEDIVIDER);
      // Serial.println(Freq);
      D++;
    }
    DeltaTime = millis() - TimeCheck;
    // std::cout << "DeltaTime = " << DeltaTime << std::endl;
    if (DeltaTime > STATETIME) {
      // Determining Next State
      StateIndex = Weigh(BetaDist);
      Clocked = false;
      DeltaTime = 0;
    }
    break;


    case 2: // Mu
    if (!Clocked) {
      Clocked = true;
      // Timing
      TimeCheck = millis();
      DeltaTime = 0;
      DeltaFreq = Freq;
      D = 0;
      // Setting Frequency
      // Freq = StateFrequencies[StateIndex];
      Serial.println("STATE = Mu");
      // std::cout << "STATE = Mu" << std::endl;
    }
    // Gradual change from one state into another.
    if (D < CHANGEDIVIDER) {
      Freq = Freq + ((StateFrequencies[StateIndex] - DeltaFreq)/CHANGEDIVIDER);
      // Serial.println(Freq);
      D++;
    }
    DeltaTime = millis() - TimeCheck;
    // std::cout << "DeltaTime = " << DeltaTime << std::endl;
    if (DeltaTime > STATETIME) {
      // Determining Next State
      StateIndex = Weigh(MuDist);
      Clocked = false;
      DeltaTime = 0;
    }
    break;

    case 3: // Alpha
    if (!Clocked) {
      Clocked = true;
      // Timing
      TimeCheck = millis();
      DeltaTime = 0;
      DeltaFreq = Freq;
      D = 0;
      // Freq = StateFrequencies[StateIndex];
      Serial.println("STATE = Alpha");
      // std::cout << "STATE = Alpha" << std::endl;
    }
    // Gradual change from on state into another
    if (D < CHANGEDIVIDER) {
      Freq = Freq + ((StateFrequencies[StateIndex] - DeltaFreq)/CHANGEDIVIDER);
      // Serial.println(Freq);
      D++;
    }
    DeltaTime = millis() - TimeCheck;
    // std::cout << "DeltaTime = " << DeltaTime << std::endl;
    if (DeltaTime > STATETIME) {
      // Determining Next State
      StateIndex = Weigh(AlphaDist);
      Clocked = false;
      DeltaTime = 0;
    }
    break;

    case 4: // Theta
    if (!Clocked) {
      Clocked = true;
      // Timing
      TimeCheck = millis();
      DeltaTime = 0;
      DeltaFreq = Freq;
      D = 0;
      // Setting Frequency
      // Freq = StateFrequencies[StateIndex];
      Serial.println("STATE = Theta");
      // std::cout << "STATE = Theta" << std::endl;
    }
    // Gradual change from on state into another
    if (D < CHANGEDIVIDER) {
      Freq = Freq + ((StateFrequencies[StateIndex] - DeltaFreq)/CHANGEDIVIDER);
      // Serial.println(Freq);
      D++;
    }
    DeltaTime = millis() - TimeCheck;
    // std::cout << "DeltaTime = " << DeltaTime << std::endl;
    if (DeltaTime > STATETIME) {
      // Determining Next State
      StateIndex = Weigh(ThetaDist);
      Clocked = false;
      DeltaTime = 0;
    }
    break;

    case 5: // Delta
    if (!Clocked) {
      Clocked = true;
      // Timing
      TimeCheck = millis();
      DeltaTime = 0;
      DeltaFreq = Freq;
      D = 0;
      // Setting Frequency
      // Freq = StateFrequencies[StateIndex];
      Serial.println("STATE = Delta");
      // std::cout << "STATE = Delta" << std::endl;
    }
    // Gradual change from one state to the next
    if (D < CHANGEDIVIDER) {
      Freq = Freq + ((StateFrequencies[StateIndex] - DeltaFreq)/CHANGEDIVIDER);
      // Serial.println(Freq);
      D++;
    }
    DeltaTime = millis() - TimeCheck;
    //std::cout << "DeltaTime = " << DeltaTime << std::endl;
    if (DeltaTime > STATETIME) {
      // Determining Next State
      StateIndex = Weigh(DeltaDist);
      Clocked = false;
      DeltaTime = 0;
    }
    break;
  }


  // THE BLINKING FUNCTIONALITY (ATM NeoPixel Functionality has been commented out.)
  ring.clear();

  ring.show(); // Begin NeoPixel Input Block
  for (int i = 0; i < 10; i++){
    CircuitPlayground.setPixelColor(i, 255, 255, 255); // OnBoard NeoPixels on - WHITE    
  }
  for (int i = 0; i < 24; i++){
    ring.setPixelColor(0, 255, 255, 255);
    ring.setPixelColor(i, 255, 255, 255); // externals
    Serial.println(i);
    ring.setBrightness(255);
  }
  ring.show(); // End NeoPixel Input Block

  ring.show(); // Begin NeoPixel Input Block
  delay(Freq);
  for (int i = 0; i < 24; i++){
    ring.setPixelColor(0, 0, 0, 0); // There was a bug - even though the increment counts 0 - 23 - the board only register pixel 0 by specifying hard like this.
    ring.setPixelColor(i, 0, 0, 0); // externals
    ring.setBrightness(0);
  }
  CircuitPlayground.clearPixels(); // Clears onboard neopixels
  ring.show(); // End NeoPixel Input Block

  ring.clear();
  delay(Freq);

}
