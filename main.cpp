#include <Arduino.h> 
#include <Adafruit_NeoPixel.h>

#define PIN_LED       4
#define PIN_BEAM      3
#define PIN_NEO_PIXEL 2  
#define NUM_PIXELS    64   

bool beadPresent = false; 
bool modeSet = false; 

Adafruit_NeoPixel NeoPixel(NUM_PIXELS, PIN_NEO_PIXEL, NEO_GRB + NEO_KHZ800);

void beamBroken(){
  beadPresent = true;
}

void setup() {
  //setup inputs and outputs 
  pinMode(PIN_LED, OUTPUT); 
  pinMode(PIN_BEAM, INPUT_PULLUP); 

  //attach hardware interrupt to the break beam sensor
  attachInterrupt(digitalPinToInterrupt(PIN_BEAM), beamBroken, FALLING);

  //begin serial communication 
  Serial.begin(9600); 

  //setup light strip
  NeoPixel.begin(); 
  NeoPixel.clear();

  //once a 1 is read from raspberry pi, begin control sequence 
  while(!modeSet){
    String data = Serial.readStringUntil('\n'); 
    if(data == "1"){
      //set which lights should turn on 
      for (int pixel = 0; pixel < NUM_PIXELS; pixel++) {  
        if(pixel % 2 == 0){
          NeoPixel.setPixelColor(pixel, NeoPixel.Color(220, 220, 255));
        } 
      }
      //set brightness and turn on the lights 
      NeoPixel.setBrightness(35); 
      NeoPixel.show();
      modeSet = true; 
    }
  }
}

void loop() {  
  if(beadPresent){
    digitalWrite(PIN_LED, HIGH); 
    delay(500); 
    digitalWrite(PIN_LED, LOW); 
    beadPresent = false;
    Serial.print("1"); 
  }
}
