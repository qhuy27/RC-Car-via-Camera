#from flask import render_template, request, Response from object import sensor_range, object_detection
import _thread
from gpiozero import Robot
#import encoder_straight as encoder
import object as sensor
#import object as ob
import RPi.GPIO as GPIO
import time
""" Camera """
import io
import picamera
import logging
import socketserver
import threading
from http import server
import pan_tilt

with open('templates/index1.html', 'r') as f:
	PAGE = f.read()


r = Robot((20,21,16),(22,23,24))
#sensor.init_sensor()
#encoder.init_robot()
#encoder.init_encoder()
speed_l = 0.8
speed_r = 0.8

def up_side():
	global speed_l, speed_r
#	ref_speed_l = 300
#	ref_speed_r = 300
#	r.value = (speed_l, speed_r)
	r.value = (speed_l,speed_r)
def down_side():
#	global ref_speed_l, ref_speed_r
#	ref_speed_l = -0.2
#	ref_speed_r = -0.2
	r.value = (-0.5, -0.5)
#	r.backward()
def right_side():
#	global ref_speed_l, ref_speed_r
#	ref_speed_l = 0.1
#	ref_speed_r = -0.1
	r.value = (0.15, -0.15)
#	r.right()
def left_side():
#	global ref_speed_l, ref_speed_r
#	ref_speed_l = -0.2
#	ref_speed_r = 0.2
	r.value = (-0.15, 0.15)
#	r.left()
def stop():
#	global ref_speed_l, ref_speed_r
#	ref_speed_l = 0
#	ref_speed_r = 0
	r.stop()

def speed_low():
	global speed_l, speed_r
	speed_l = 0.6
	speed_r = 0.6
def speed_medium():
	global speed_l, speed_r
	speed_l = 0.8
	speed_r = 0.8
def speed_high():
	global speed_l, speed_r
	speed_l = 1
	speed_r = 1

class StreamingOutput(object):
	def __init__(self):
		self.frame = None
		self.buffer = io.BytesIO()
		self.condition = threading.Condition()

	def write(self, buf):
		if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
			self.buffer.truncate()
			with self.condition:
				self.frame = self.buffer.getvalue()

				self.condition.notify_all()
			self.buffer.seek(0)
		return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/':
			self.send_response(301)
			self.send_header('Location', '/index.html')
			self.end_headers()
		elif self.path == '/index.html':
			content = PAGE.encode('utf-8')
			self.send_response(200)
			self.send_header('Content-Type', 'text/html')
			self.send_header('Content-Length', len(content))
			self.end_headers()
			self.wfile.write(content)
		elif self.path == '/up_side':
			up_side()
		elif self.path == '/down_side':
			down_side()
		elif self.path == '/left_side':
			left_side()
		elif self.path == '/right_side':
			right_side()
		elif self.path == '/stop':
			stop()
		elif self.path == '/speed_low':
			speed_low()
		elif self.path == '/speed_medium':
			speed_medium()
		elif self.path == '/speed_high':
			speed_high()
#		elif self.path == '/stream.mjpg':
#			self.send_response(200)
#			self.send_header('Age', 0)
#			self.send_header('Cache-Control', 'no-cache, private')
#			self.send_header('Pragma', 'no-cache')
#			self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
#			self.end_headers()
#			try:
#				while True:
#					with output.condition:
#						output.condition.wait()
#						frame = output.frame
#					self.wfile.write(b'--FRAME\r\n')
#					self.send_header('Content-Type', 'image/jpeg')
#					self.send_header('Content-Length', len(frame))
#					self.end_headers()
#					self.wfile.write(frame)
#					self.wfile.write(b'\r\n')
#			except Exception as e:
#				logging.warning(
#					'Removed streaming client %s: %s',
#					self.client_address, str(e))
		elif self.path == '/pan/30':
			pan_tilt.move('pan', 30)
		elif self.path == '/pan/45':
			pan_tilt.move('pan', 45)
		elif self.path == '/pan/60':
			pan_tilt.move('pan', 60)
		elif self.path == '/pan/75':
			pan_tilt.move('pan', 75)
		elif self.path == '/pan/90':
			pan_tilt.move('pan', 90)
		elif self.path == '/pan/105':
			pan_tilt.move('pan', 105)
		elif self.path == '/pan/120':
			pan_tilt.move('pan', 120)
                #TILT
		elif self.path == '/tilt/30':
			pan_tilt.move('tilt', 30)
		elif self.path == '/tilt/45':
			pan_tilt.move('tilt', 45)
		elif self.path == '/tilt/60':
			pan_tilt.move('tilt', 60)
		elif self.path == '/tilt/75':
			pan_tilt.move('tilt', 75)
		elif self.path == '/tilt/90':
			pan_tilt.move('tilt', 90)
		elif self.path == '/tilt/105':
			pan_tilt.move('tilt', 105)
		elif self.path == '/tilt/120':
			pan_tilt.move('tilt', 120)
		else:
			self.send_error(404)
			self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
	allow_reuse_address = True
	daemon_threads = False

def run_PID():
	global ref_speed_l, ref_speed_r
	while True:
		encoder.PID(ref_speed_l, ref_speed_r)

def run_Sensor():
	while True:
		print(sensor.object_detection())

#output = StreamingOutput()
#address = ('', 5010)
#server = StreamingServer(address, StreamingHandler)
#server.serve_forever()
#thread = threading.Thread(target = run_PID, args = ( ) )
#thread.start()

#thread = threading.Thread(target = run_PID, args = ( ) )
#thread.start()

with picamera.PiCamera(resolution='320x240', framerate=20) as camera:
	output = StreamingOutput()

    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
	camera.start_recording(output, format='mjpeg')
	try:
#		thread = threading.Thread(target = run_Sensor, args = ( ) )
#		thread.start()
		address = ('', 5010)
		server = StreamingServer(address, StreamingHandler)
		server.serve_forever()
	finally:
		camera.stop_recording()
