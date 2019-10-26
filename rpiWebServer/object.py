import RPi.GPIO as GPIO
import time

class Sensor():

	def __init__(self, Trig, Echo):
		self.Trig = Trig
		self.Echo = Echo
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.Trig,GPIO.OUT)
		GPIO.setup(self.Echo,GPIO.IN)

#function to measure range
	def sensor_range(self):
		#global TRIG
		#global ECHO
		#GPIO.setmode(GPIO.BCM)
		init_sensor()
		GPIO.output(self.Trig, GPIO.LOW)
		time.sleep(0.5)

		GPIO.output(self.Trig, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(self.Trig, GPIO.LOW)

		while GPIO.input(self.Echo) == 0:
			pulse_start = time.time()
		while GPIO.input(self.Echo) == 1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		GPIO.cleanup()
		return distance

def init_sensor():
	global Sen
	Sen = Sensor(13, 12)


def object_detection():
	global Sen
	distance = Sen.sensor_range()
	if distance > 10:
		print('True')
		return True
	print('False')
	return False 

#while (True):
#	print(object_detection())
