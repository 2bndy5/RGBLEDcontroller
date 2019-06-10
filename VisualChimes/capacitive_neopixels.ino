// #include "Adafruit_MPR121.h"
#include <Adafruit_NeoPixel.h>
#include <math.h>
#include <SPI.h>
#include <RF24.h>
#include "Colour.h"
#include "Ripple.h"

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN            6
// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      12
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRBW + NEO_KHZ800);
//array of colors to manipulate each independently
Colour arr[NUMPIXELS + 1];// defaults to white @ half intensity

// Adafruit_MPR121 cap = Adafruit_MPR121();
// Keeps track of the last pins touched
// so we know when buttons are 'released'
// uint16_t lasttouched = 0;
// uint16_t currtouched = 0;


// bits for enqueing commands for transmission
unsigned char controls[32] = {52, 102, 202, '1'};
/*  pot1*4/5,  pot2*4/5, pot2pot1*1/5 + toggles, mode[0-255]
* B 1111 1111, 0000 0000, 	0011 		0010,	 0000 0000	
* controls[2] bit 1 is toggle for ripple effect 
* controls[2] bit 0 is toggle for single [true = 1] or multiple [false = 0] colors per pixel
*/

Ripple effect(NUMPIXELS); // object for controling ripple effect and determining initial segment solor

RF24 radio(7, 8);// create radio
byte addresses[][6] = {"1Node","2Node"};

//function declarations
bool go2norm(uint8_t i);
bool cycleHue(uint8_t i);
void setAllI(double x);
void drawPixels();

void setup() {

	Serial.begin(9600);
	// Default address is 0x5A, if tied to 3.3V its 0x5B
	// If tied to SDA its 0x5C and if SCL then 0x5D
	// if (!cap.begin(0x5A)) {
		// Serial.println("MPR121 not found, check wiring?");
		// while (true);
	// }
	
	
	radio.begin();
	radio.setPALevel(RF24_PA_LOW);// for prototyping only, delete this line when done
	// radio.setChannel(108);
	

	pixels.begin(); // This initializes the NeoPixel library.
	drawPixels();
}

bool rxData(){
	radio.openReadingPipe(1, addresses[0]);
	radio.startListening();
	if(radio.available()){
		radio.read(&controls,sizeof(controls));
		radio.stopListening();
		return true;
	}
	else{
		radio.stopListening();
		return false;
	} 
}

void printControls(){
	for (uint8_t i = 0; i < 4; i++){
		for (int8_t j = 7; j >= 0; j--){
			if (controls[i] & (1 << j))
				Serial.print('1');
			else Serial.print('0');
		}
		if (i < 3)
			Serial.print(' ');
		else Serial.println();
	}
}

void loop() {
	bool updated = rxData();

	effect.royGbiv = (controls[2] & 1);
	effect.setRipple(controls[2] & 2); 
	double idleI = (controls[0]+((controls[2] & 192) << 2)) / 1023.0;
	setAllI(idleI);
	short idleHue = (controls[1]+((controls[2] & 48) << 4)) / 1023.0 * 360;
	bool idleSat = idleHue > 0 ? 1 : 0;
	arr[NUMPIXELS + 1].setH(idleHue);
	arr[NUMPIXELS + 1].setS(idleSat);

	if (updated){
		Serial.print("settings change received, controls = ");
		printControls();
		// Serial.print("royGbiv = ");
		// Serial.print(controls[2] & 1);
		// Serial.print(", ");
		// Serial.print("ripple = ");
		// Serial.print(controls[2] & 2);
		// Serial.print(", ");
		// Serial.print("brighness = ");
		// Serial.print(idleI);
		// Serial.print("idle hue = ");
		// Serial.println(idleHue);
	}
	// else Serial.println("nothing recieved");
	
	// Get the currently touched pads
	// currtouched = cap.touched();
	
	bool needDraw = false;
	for (uint8_t i = 0; i < NUMPIXELS; i++){
		if (!effect.royGbiv && (cycleHue(i) || go2norm(i))) 
			needDraw = true;
		else if (go2norm(i)) 
			needDraw = true;
	}
	if (effect.nextStage()){
		arr[effect.getL()].setColorI(255);
		arr[effect.getR()].setColorI(255);
		arr[effect.getL()].setH(effect.getColor());
		arr[effect.getR()].setH(effect.getColor());
	}
	if (needDraw) drawPixels();
	// if (!(controls[2] & 2) || (!needDraw && (controls[2] & 2))){
		// for (uint8_t i = 0; i < NUMPIXELS; i++){
			// if it *is* touched and *wasnt* touched before, alert!
			// if ((currtouched & _BV(i)) && !(lasttouched & _BV(i)) ) {
				// effect.setStart(i);
				// arr[i].setColorI(255);
				// arr[i].setH(effect.getColor());
			// }
		// }
	// }
	// updates all led's color if values have changed
  // reset our state of touchpads
  // lasttouched = currtouched;
}// end main loop

//returns true if neopixel's color value has changed
bool go2norm(uint8_t i){
	if ((!effect.royGbiv && (arr[i].getH() >= 300)) || effect.royGbiv){
		unsigned char c = arr[i].getColorI();
		if ((effect.royGbiv && c >= 128))
			arr[i].setColorI(c-11); 
		else if (c)
			arr[i].setColorI(0);
		else return c;
	}
	else return false;	
}

// checks neopixels' hue value and increments (by 30 if hue <= 330) through spectrum
//returns true if neopixel's color value has changed
bool cycleHue(uint8_t i){
	if ((controls[2] & 2) && effect.getStage() && (i == effect.getL() || i == effect.getR())){
		return true;
	}
	else if (arr[i].getH() <= 330){
		arr[i].setH(!arr[i].getH() ? 1 : arr[i].getH() + 30);
		return true;
	}
	else return false;
}

void setAllI(double x){
	for (int8_t i = 0; i < NUMPIXELS + 1; i++)
		arr[i].setI(x);
}

void drawPixels(){
	bool idleSat = arr[NUMPIXELS + 1].getH() > 0 ? 1 : 0;
	for (uint8_t i = 0; i < NUMPIXELS; i++){
		if (arr[i].getColorI() > 170)// if white set to off
			pixels.setPixelColor(i, arr[i].getR(), arr[i].getG(), arr[i].getB(), 0);
		else if (arr[i].getColorI() == 0)// if pixel is idle
			pixels.setPixelColor(i, idleSat * arr[NUMPIXELS + 1].getR(), idleSat * arr[NUMPIXELS + 1].getG(), idleSat * arr[NUMPIXELS + 1].getB(), (1 - idleSat) * arr[NUMPIXELS + 1].getColorI());
		else // used when fading to idle
			pixels.setPixelColor(i, arr[i].getR(), arr[i].getG(), arr[i].getB(), (255 - arr[i].getColorI()) * (1 - idleSat));
	}
	pixels.show();
	delay((controls[2] & 2) ? 55 : 83);//need to fix this from causing interupt
}
