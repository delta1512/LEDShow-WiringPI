import wiringpi2 as wpi
import sys
import time
import random

#Change GPIO addresses for LEDs here
global leds, ledlen
leds = [2, 0, 1, 4, 5, 6, 10, 11, 26, 27]
ledlen = len(leds)

#check for even arrangement
if ledlen % 2 != 0:
	print('ERROR: Number of LEDs is uneven: ' + ledlen)
	sys.exit()

#pattern calculators
global updownbin, rollbin, wigglebin, rotatebin, wavebin
updownbin = []
wigglebin = []
rotatebin = [0, 0, 1, 1, 1, 1, 0, 0]
wavebin = [1, 1]
#updown and roll
for x in range(0, ledlen): #update names when done
	updownbin.append(0)
rollbin = updownbin
#wiggle
for x in range(0, ledlen):
	wigglebin.append(1)
wigglebin[0], wigglebin[ledlen-1] = 0, 0
#rotate
while len(rotatebin) < ledlen:
	rotatebin.insert(int(round(len(rotatebin) / 2)), 0)
#wave
while len(wavebin) < ledlen:
	wavebin.insert(0, 0)
	wavebin.insert(len(wavebin), 0)

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
		print('ERROR: Incorrect LED assignment in function: ' + n)
		sys.exit()

#Increment from one end to another and then reverse
def updown():
	name = 'updown()'
	binout = updownbin
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

#Increment from one end to another and then decrement from the origin
def roll():
	name = 'roll()'
	binout = rollbin
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
#Another loop (using the first number) generates a number between 0 and power 2
#of the total bits and displays it on the LEDs
def rand():
	n = random.randint(10, 100)
	for x in range(0, n):
		i = random.randint(0, (2**ledlen) - 1)
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
	binout = wigglebin
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
	binout = rotatebin
	check(binout, name)
	for x in range(0, ledlen * 2):
		write(binout)
		binout.insert(0, binout[ledlen - 1])
		del binout[ledlen]
		time.sleep(0.1)
	clr()

#Two LEDs from the center travel outwards, bounce off the edges and meet back
#in the center 3 times
def wave():
	name = 'wave()'
	binout = wavebin
	check(binout, name)
	constp = ledlen - 1
	a = -1
	b = (ledlen / 2)
	for x in range(0, 3):
		write(binout)
		time.sleep(0.15)
		while b != constp:
			b = b + 1
			a = constp - b
			binout[a] = 1
			binout[b] = 1
			binout[a + 1] = 0
			binout[b - 1] = 0
			write(binout)
			time.sleep(0.15)
		while b != (ledlen / 2):
			b = b - 1
			a = constp - b
			binout[a] = 1
			binout[b] = 1
			binout[a - 1] = 0
			binout[b + 1] = 0
			write(binout)
			time.sleep(0.15)
	clr()

#Call your functions here
#Use the for loop if you wish or use "while True:" statement to loop forever
for i in range(0, 1):
	updown()
	roll()
	wiggle()
	rotate()
	wave()
	rand()
