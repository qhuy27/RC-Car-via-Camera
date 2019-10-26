import os
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90
from flask import render_template
#set pin for pan-tilt
panPin = 19
tiltPin = 26

def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		panServoAngle = int(angle)
		os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		tiltServoAngle = int(angle)
		os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
	
	templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}

