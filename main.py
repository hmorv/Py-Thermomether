from Tkinter import * #GUI
import RPi.GPIO as GPIO
import time, math

C = 0.38
R1 = 1000
B = 3800.0 #thermistor constant
R0 = 1000.0

GPIO.setmode(GPIO.BCM) # Broadcom pin names

pinA = 18 # charges the capacitor through a fixed 1k resistor and a thermistor in series
pinB = 23 # discharges the capacitor through a fixed 1k resistor

def discharge(): #empty the capacitor
	GPIO.setup(pinA, GPIO.in)
	GPIO.setup(pinB, GPIO.out)
	GPIO.output(pinB, false)
	time.sleep(0.01)

# return the time taken for the voltage 
def chargeTime():
	GPIO.setup(pinB, GPIO.in)
	GPIO.setup(pinA, GPIO.out)
	GPIO.output(pinA, True)
	t1 = time.time()
	while not GPIO.input(pinB):
		pass
	t2 = time.time()
	return (t2-t1) * 1000000 #microseconds

def readResistance():
	n = 10
	total = 0
	for i in range(0,n):
		total = total + analogRead()
	t = total / float(n)
	T = t * 0.632 * 3.3
	r = (T/C) - R1
	return r

def analogRead():
	discharge()
	t = chargeTime()
	discharge()
	return t

def readTempInCelsius():
	R = readResistance()
	t0 = 273.15
	t25 = t0 + 25.0
	invT = 1/t25 + 1/B * math.log(R/R0)
	T = (1/invT - t0)
	return T

class App:

	def __init__(self, master):
		self.master = master
		frame = Frame(master)
		frame.pack()