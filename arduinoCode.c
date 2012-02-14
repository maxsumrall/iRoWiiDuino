/*
Jonathan Sumrall
George Mason University, Fall 2010
CS101
Professor Luke
Final Project

This is the code that the Arduino board runs.

The basic operation is that the board listens on the serial port for data. It
recieves that data and does basic servo movements depending on which 
case the data is. 


HOW TO USE:
	With hardware correctly setup, upload this code to the arduino and 
	open up the serial connection on the arduino program on your PC
	or via some other program you wrote and send it strings of characters.
	So if you open up the serial console and type 2,3,4,5,6,p,l,o,k, there
	will be an action on the arduino. To figure out what these numbers are 
	corrosponding to in the switch statement, take the ord() or the string.
	*/









#include 
/*initial position of the servos*/
int posX1 = 90;
int posX2 = 90;

Servo y1Servo,y2Servo,x1Servo,x2Servo;
int val;
int incomingByte = 0;	// for incoming serial data

void setup() {
	/*the arduino runs this code once and moves on to loop() 
	the attach method specifies which pin the servo is located on*/
	
	
	x1Servo.attach(7);
	x2Servo.attach(6);
	y1Servo.attach(5);
	y2Servo.attach(4);
	

	Serial.begin(9600);// opens serial port, sets data rate to 9600 bps
}

void loop() {
	  /*Listen in on the serial port*/
	 int x = Serial.read();
	
	/*Special case to make sure the X axis servos stay in range*/
	
	/*It stops the servos from going past these certian ranges 
	These servos move to certian degrees from 0 to 180. Just to be safe I 
	limited it to 10 and 160
	*/
	if(posX1 >160){posX1 = 160;posX2 = 10;}
	if(posX1 < 20){posX1 = 20; posX2 = 170;}
	
	
	 
	/*Scale the input numbers: input of 2 = 50, 3 = 51, 4 = 52 etc...
	take the ord() of the character you're sending in the python code and 
	that value is the value that the arduino will get. So where the code 
	says 50,51, etc, those are key values from the seial ord'ed by 
	the arduino. Im sure theres another name for it...
	
	*/
	switch (x) {	    
		case 50:
			/*open or close hands*/
			posX1++;
			posX2--;	      
			x1Servo.write(posX1);
			x2Servo.write(posX2);
			break;
		
		
		case 51:
			/*open or close hands*/
			posX1--;
			posX2++;
			x1Servo.write(posX1);
			x2Servo.write(posX2);
			break;
		
		case 52:
			/*Move hands up or down*/
			y1Servo.write(85);
			y2Servo.write(105);
			/*These servos have no potentiometer.
			They are continous rotation. 
			You must turn then on for a time,
			then turn them off. 
			It is up to the user to make sure
			not to over-extend them. */
			
			delay(50);
			
			/*Now, im turning them off.
			A value of 95 is its neutral position.
			So they stop */
			
			y1Servo.write(95);
			y2Servo.write(95);
			break;
		    
		
		
		case 53:	
			/* move hands up or down*/
			y1Servo.write(105);
			y2Servo.write(85);
			/*These servos have no potentiometer.
			They are continous rotation. 
			You must turn then on for a time,
			then turn them off. 
			It is up to the user to make sure
			not to over-extend them. */
			
			delay(50);
			
			/*Now, im turning them off.
			A value of 95 is its neutral position.
			So they stop */
			
			y1Servo.write(95);
			y2Servo.write(95);
			break;
		
		case  112:
			/*move servo y1 up or down*/
			y1Servo.write(105);
			delay(50);
			y1Servo.write(95);
			break;

		case  108:
			/*move servo y1 up or down*/
			y1Servo.write(85);
			delay(50);
			y1Servo.write(95);
			break;
		
		case  107:
			/*mvoe servo y2 up or down */
			y2Servo.write(105);
			delay(50);
			y2Servo.write(95);
			break;
		
		case  111:
			/*move servo y2 up or down */
			y2Servo.write(85);
			delay(50);
			y2Servo.write(95);
			break;
	}
	
	/*Reset the data recieved off the serial port*/	     
	x = 0;
}

