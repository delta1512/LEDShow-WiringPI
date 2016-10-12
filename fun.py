import wiringpi2 as wpi
import sys
import time
import random

'''
Some functions require customised LED assignment to operate normally

***This version is untested***
'''

#Change GPIO addresses for LEDs here
global leds
leds = [2, 0, 1, 4, 5, 6, 10, 11, 26, 27]
global ledlen
ledlen = len(leds)

wpi.wiringPiSetup()

#Setup and clear LEDs
for x in leds:
	wpi.pinMode(x, 1)
	wpi.digitalWrite(x, 0)

#Function for clearing the LEDs
def clr():
	for x in leds:
		wpi.digitalWrite(x, 0)

#Function for writing an array as the LED output
#Call the function with an input array of ten 1s or 0s
def write(a):
	y = 0
	for x in leds:
		wpi.digitalWrite(x, a[y])
		y = y + 1

#Check for correct length in LED assignment
def check(a, n):
	if len(a) != ledlen:
		print('Incorrect LED assignment in function: ' + n)
		sys.exit()

#increment from one end to another and then reverse
def updown():
	name = 'updown()'
	binout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	check(binout, name)
	for x in range(0, ledlen):
		binout[x] = 1
		write(binout)
		time.sleep(0.1)
	for x in range(1, ledlen + 1):
		binout[10 - x] = 0
		write(binout)
		time.sleep(0.1)
	clr()

#increment from one end to another and then decrement from the origin
def lftright():
	name = 'lftright()'
	binout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	check(binout, name)
	for x in range(1, ledlen + 1):
		binout[10 - x] = 1
		write(binout)
		time.sleep(0.1)
	for x in range(1, ledlen + 1):
		binout[10 - x] = 0
		write(binout)
		time.sleep(0.1)
	clr()

#Generates a number between 1 and 100 which defines how many times it will loop
#Another loop (using the first number) generates a number between 0 and 1023 and displays it on the LEDs
def rand():
	n = random.randint(10, 100)
	for x in range(0, n):
		i = random.randint(0, 1023)
		binout = []
		while i >= 1:
			mod = i%2
			binout.append(mod)
			i = i // 2
		while len(binout) != ledlen:
			binout.append(0)
		write(binout)
		time.sleep(0.1)
	clr()
	
#Array is shifted left and right, a value is deleted when it hits either end
def wiggle():
	name = 'wiggle()'
	binout = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
	check(binout, name)
	while sum(binout) != 0:
		while binout[ledlen - 1] != 1:
			binout.insert(0, 0)
			del binout[ledlen]
			write(binout)
			time.sleep(0.1)
		binout[ledlen - 1] = 0
		while binout[0] != 1:
			binout.insert(10, 0)
			del binout[0]
			write(binout)
			time.sleep(0.1)
		binout[0] = 0
	clr()
	
#Shifts (with rotation) the array multiple times
def rotate():
	name = 'rotate()'
	binout = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
	check(binout, name)
	for x in range(0, ledlen * 2):
		write(binout)
		binout.insert(0, binout[ledlen - 1])
		del binout[ledlen]
		time.sleep(0.1)
	clr()
	
#Two LEDs from the center travel outwards, bounce off the edges and meet back in the center
def wave():
	name = 'wave()'
	binout = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
	check(binout, name)
	for x in range(0, 3):
		a = 5
		b = 4
		c = 4
		d = 5
		for y in range(0, 5):
			write(binout)
			binout[a] = 0
			binout[b] = 0
			binout[c] = 1
			binout[d] = 1
			a = a - 1
			b = b + 1
			c = c - 1
			d = d + 1
			if d == 10:
				d = 9
			time.sleep(0.1)
		write(binout)
		a = 0
		b = 9
		c = 1
		d = 8
		for z in range(0, 5):
			binout[a] = 0
			binout[b] = 0
			binout[c] = 1
			binout[d] = 1
			time.sleep(0.1)
			write(binout)
			a = a + 1
			b = b - 1
			c = c + 1
			d = d - 1
	clr()

#Call your functions here 
#Use the for loop if you wish or use "while True:" statement to loop forever
for i in range(0, 5):
	updown()
	lftright()
	wiggle()
	rotate()
	wave()
	rand()
