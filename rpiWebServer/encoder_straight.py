
from RPi import GPIO
from time import sleep
from gpiozero import Robot

class Encoder():

	def __init__(self, pin_A, pin_B):
		self.pin_A = pin_A
		self.pin_B = pin_B
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.pin_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.counter = 0
		self.Last_State = GPIO.input(self.pin_A)

	def count_tick(self,channel):
		self.counter +=1

	def reset(self):
		self.counter = 0

	@property
	def value(self):
		return self.counter

KP = 1/2000
KD = 0*1/200000
KI = 0*1/400000

e1_prev_error = 0
e2_prev_error = 0
speed_l = 0
speed_r = 0
e1_sum_error = 0
e2_sum_error = 0

def init_encoder():
	global left, right
	left = Encoder(17, 18)
	right  = Encoder(5 , 6)

	GPIO.add_event_detect(17, GPIO.RISING  , callback=left.count_tick)
	GPIO.add_event_detect(6 , GPIO.RISING  , callback=right.count_tick)


def init_robot():
	global r
	r = Robot((20,21,16),(22,23,24))

def reset_PID():
	global KD
	global speed_l, speed_r
	global e1_prev_error, e2_prev_error
	global e1_sum_error, e2_sum_error
	KD = 0
	speed_l = 0
	speed_r = 0
	e1_prev_error = 0
	e2_prev_error = 0
	e1_sum_error = 0
	e2_sum_error = 0

def PID(ref_speed_l, ref_speed_r):
	global KP, KD, KI
	global e1_prev_error, e2_prev_error
	global e1_sum_error, e2_sum_error
	global speed_l, speed_r
	global left, right

	if (ref_speed_l>0 and ref_speed_r>0):
#		print("-------------")
		left_error = ref_speed_l - left.value
		right_error = ref_speed_r - right.value
		if (speed_l !=0 or speed_r != 0):
			KD = KD * (speed_l+speed_r)/2
#		print("r_er             {}              l_er            {}".format(right_error, left_error))
		speed_l += (left_error * KP)  + (e1_prev_error * KD) + (e2_sum_error * KI)
		speed_r += (right_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
#		print("speed_r          {}              speed_l         {}".format(speed_r, speed_l))
		if (speed_l > 1):
			speed_l = 1
		if (speed_r > 1):
			speed_r = 1
		r.value = (speed_l, speed_r)

#		print("right            {}              left            {}".format(right.value, left.value))
#		print("ref_r            {}              ref_l           {}".format(ref_speed_r, ref_speed_l))

		right.reset()
		left.reset()

		sleep(0.2)

		e1_prev_error = left_error
		e2_prev_error = right_error

		e1_sum_error += left_error
		e2_sum_error += right_error
	else:
		r.value = (ref_speed_l, ref_speed_r)
		left.reset()
		right.reset()
		reset_PID()

