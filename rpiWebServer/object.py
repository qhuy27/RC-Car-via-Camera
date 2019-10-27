import RPi.GPIO as GPIO
import time

class Sensor():
	
	#function to initializes the sensor
	#param(Trig, Echo)
	#Trig: the pin for your Trigger Pulse Input (TRIG)
	#Echo: the pin for your Echo Pulse Output (ECHO)
	def __init__(self, Trig, Echo):
		self.Trig = Trig
		self.Echo = Echo
		GPIO.setmode(GPIO.BCM)
		#setup the TRIG pin
		GPIO.setup(self.Trig,GPIO.OUT)
		#setup the ECHO pin
		GPIO.setup(self.Echo,GPIO.IN)

	#function to measure range
	def sensor_range(self):
		
		#initialize the sensor
		init_sensor()
		GPIO.output(self.Trig, GPIO.LOW)
		#wait for the sensor to settle
		time.sleep(0.5)
		
		#send out pulse signal
		GPIO.output(self.Trig, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(self.Trig, GPIO.LOW)

		#timestamp when the pulse is sent
		while GPIO.input(self.Echo) == 0:
			pulse_start = time.time()
		#timestamp when the pulse is received
		while GPIO.input(self.Echo) == 1:
			pulse_end = time.time()
			
		#duration of the pulse
		pulse_duration = pulse_end - pulse_start
		#distance calculated using the formula
		distance = pulse_duration * 17150
		#round the distance to 2 decimal places
		distance = round(distance, 2)
		#clean GPIO pins to reset inputs/outputs
		GPIO.cleanup()
		return distance

#set up the sensor
def init_sensor():
	global Sen
	Sen = Sensor(13, 12)

#function to detect object
def object_detection():
	global Sen
	#taking the distance measured from the sensor
	distance = Sen.sensor_range()
	if distance > 10:
		print('True')
		return True
	print('False')
	return False 

