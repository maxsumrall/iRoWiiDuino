#main.py
#
#Jonathan Sumrall
#George Mason University, Fall 2010
#CS101
#Professor Luke
#Final Project
#
#


#This is the main file.
#Connect to the wii remote, the arduino, and the create. 
#
#From there, its basically a large switch statement. For various button presses 
#there are different cases to carry out. 


import create
import cwiid #The wiimote python bluetooth library
import time


def main():
	ser,robot = makeConnections()
	wii = connectWiimote()	
	
	
	#Constants to change the speed of the robot when using the D-PAD
	vel = 20
	rad = 20
	
	
	print "\n\niRobot Activated"
	while(1):	
		
		
		#The button pressed is reported as an integer.
		#Trigger = 4
		#UP arrow = 2048
		#DOWN arrow = 1024
		#LEFT arrow = 256
		#RIGHT arrow = 512
		
		#So, when it says something like:
		#btnpressed == , 
		#that number is the integer the wii remotes is giving us.
		#Each button has a value. 
		#When multiple buttons are pressed, their values are added.
		#You can see this in the very first case of this.
		#2048 is the up button, 4 is the trigger. When you press both,
		#the wii tells us a value of 2052. 
		btnPressed,nunBtn = rptBtns(wii)	
		
		
		#######Drive the Create#######
					
		if (btnPressed == (2048+4)): #UP
			robot.go(vel,0)
			
		elif (btnPressed == 1024+4): #DOWN
			robot.go(-vel,0)
			
		elif (btnPressed == 256+4): #LEFT
			robot.go(0,rad)
			
		elif(btnPressed == 512+4): #RIGHT
			robot.go(0,-rad)
		
		elif ((btnPressed == 0) or (btnPressed == 4)): #STOP
			robot.go(0,0)
				
			
			
		#####Control the arduino hand#####
		#The strings we write to the arduino serial 
		#are just chosen without anyt specific reason other than
		#they are the values I programmed the arduino to expect.
		
		#just to be safe, we sleep. I'm not sure we actually need to.
		if( btnPressed == 2048):
			ser.write('4')
			time.sleep(0.1)
			
		elif(btnPressed == 1024):
			ser.write('5')
			time.sleep(0.1)
		elif(btnPressed == 256):
			ser.write('2')
			time.sleep(0.1)
		elif(btnPressed == 512):
			ser.write('3')
			time.sleep(0.1)
		
		
		#Calibration control. For when we want to control just one 
		#hand and not both.
		
		#nunBtn 1 == the nunchuk trigger
		#nunBtn 2 == another nunchuk trigger
		
		while nunBtn == 1:
			if( btnPressed == 2048):
				ser.write('p')
				time.sleep(0.1)
				
			elif(btnPressed == 1024):
				ser.write('l')
				time.sleep(0.1)
			btnPressed,nunBtn = rptBtns()	

			
		while nunBtn == 2:
			if( btnPressed == 2048):
				ser.write('o')
				time.sleep(0.1)
				
			elif(btnPressed == 1024):
				ser.write('k')
				time.sleep(0.1)
			btnPressed,nunBtn = rptBtns()	
			
			
	#Neutral X and Y position. THis way we can deal with differnt wiimotes
		nX,nY = 126,126
		#Current joystick position
		joyX,joyY = rptJoy(wii)
		
		while (joyX > nX+5) or (joyX < nX-5) or (joyY < nY-5) or (joyY > nY+5):
			#Drive the robot, with vairbale speed depending on
			#How far from center the stick on nunchuk is
			robot.go( (joyY-nY), (-1*(joyX - nX)) )
			#Reset the new current joystick position
			joyX,joyY = rptJoy(wii)

	
def rptBtns(wii):
	return wii.state.get("buttons"),wii.state.get("nunchuk").get("buttons")
	
def rptJoy(wii):
	joyX = wii.state.get("nunchuk").get("stick")[0]
	joyY = wii.state.get("nunchuk").get("stick")[1]
	return joyX,joyY
	
	
		
def connectArduino():
	try:		
		location = raw_input("Where is the Arduino board? :")
		ser = serial.Serial(('/dev/ttyUSB'+location), 9600, timeout = None)
		time.sleep(1)
		print "Connected to Arduino board\n"
		return ser
	except: 
		print "Error: Could not conenct to Arduino Board at that port."
		exit()
		
#Connect to the Irobot Create
def connect():
	try:
		loc = raw_input("Where is the iRobot Create? :")
		robot = create.Create("/dev/ttyUSB"+loc)
		print "Connected to iRobot Create\n"
		return robot
	
	except:
		print "Error: Could not connect to iRobot Create at that port."
		exit()
		
def makeConnections():
	ser = connectArduino()
	robot = connect()
	robot.toFullMode()
	return ser,robot
	
def connectWiimote():
	#Connect to the wiimote so we  can interface with it.
	print "Press 1+2 on the wiimote and press enter..."
	raw_input() #Wait for user to start the sync.
	print "Connecting..."
	
	#For this specific project with my specific wiimote, this is its MAC address. 
	#In general, you can omit any arguments to Wiimote()
	wii = cwiid.Wiimote("00:1F:32:9C:90:C0")
	#test that the wiimote is conencted by turning on a light
	wii.led = 1
	#Some magic happens and now the state method now tells us the info we want
	wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_EXT
	print "Connection established\n"
	
	return wii




main()
