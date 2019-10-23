#from flask import render_template, request, Response
#from object import sensor_range, object_detection 
import _thread
from gpiozero import Robot
import encoder_straight as encoder
import RPi.GPIO as GPIO
import time
""" Camera """
import io
import picamera
import logging
import socketserver
import threading
from http import server

with open('templates/index1.html', 'r') as f:
	PAGE = f.read()


#r = Robot((20,21,12),(22,24,25))
encoder.init_robot()
encoder.init_encoder()
#encoder.setup()
ref_speed_l = 0
ref_speed_r = 0

def up_side():
	global ref_speed_l, ref_speed_r
	ref_speed_l = 300
	ref_speed_r = 300
#	r.value = (speed_l, speed_r)
#	r.forward()
def down_side():
	global ref_speed_l, ref_speed_r
	ref_speed_l = -0.5
	ref_speed_r = -0.5
#	r.value = (-0.2, -0.2)
#	r.backward()
def right_side():
	global ref_speed_l, ref_speed_r
	ref_speed_l = 0.5
	ref_speed_r = 0
#	r.value = (0.2, 0)
#	r.right()
def left_side():
	global ref_speed_l, ref_speed_r
	ref_speed_l = 0
	ref_speed_r = 0.5
#	r.value = (0, 0.2)
#	r.left()
def stop():
	global ref_speed_l, ref_speed_r
	ref_speed_l = 0
	ref_speed_r = 0
#	r.stop()


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
		elif self.path == '/stream.mjpg':
			self.send_response(200)
			self.send_header('Age', 0)
			self.send_header('Cache-Control', 'no-cache, private')
			self.send_header('Pragma', 'no-cache')
			self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
			self.end_headers()
			try:
				while True:
					with output.condition:
						output.condition.wait()
						frame = output.frame
					self.wfile.write(b'--FRAME\r\n')
					self.send_header('Content-Type', 'image/jpeg')
					self.send_header('Content-Length', len(frame))
					self.end_headers()
					self.wfile.write(frame)
					self.wfile.write(b'\r\n')

			except Exception as e:
				logging.warning(
					'Removed streaming client %s: %s',
					self.client_address, str(e))
		else:
			self.send_error(404)
			self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
	allow_reuse_address = True
	daemon_threads = True

def run_PID():
	global ref_speed_l, ref_speed_r
	while True:
		encoder.PID(ref_speed_l, ref_speed_r)



#def thread_cam():
with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
	output = StreamingOutput()

    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
	camera.start_recording(output, format='mjpeg')
	try:
		thread = threading.Thread(target = run_PID, args = ( ) )
		thread.start()
		address = ('', 5010)
		server = StreamingServer(address, StreamingHandler)
		server.serve_forever()
	finally:
		camera.stop_recording()

