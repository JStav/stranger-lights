import time
import random
import datetime

from neopixel import *

class LightDriver:

	# LED strip configuration:
	LED_COUNT      = 50      # Number of LED pixels.
	LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
	#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
	LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
	LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

	COLOR_BLUE = Color(14, 63, 180)
	COLOR_YELLOW = Color(255, 174, 0)
	COLOR_WHITE = Color(255, 255, 255)
	COLOR_RED = Color(255, 0, 0)
	COLOR_FUCHSIA = Color(149, 12, 141)
	COLOR_MINT = Color(59, 208, 216)

	LETTERS = { 'a' : 12, 'b' : 13, 'c' : 14, 'd' : 15, 'e' : 16, 'f' : 17, 'g' : 18, 'h' : 19, 
		'i' : 31, 'j' : 30, 'k' : 29, 'l' : 28, 'm' : 27, 'n' : 26, 'o' : 25, 'p' : 24, 'q' : 23,
		'r' : 35, 's' : 36, 't' : 37, 'u' : 38, 'v' : 39, 'w' : 40, 'x' : 41, 'y' : 42, 'z' : 43 }

	COLORS = { 'a': COLOR_WHITE, 'b' : COLOR_BLUE, 'c' : COLOR_FUCHSIA, 'd' : COLOR_MINT, 'e' : COLOR_BLUE, 'f' : COLOR_YELLOW, 'g' : COLOR_RED, 'h' : COLOR_BLUE,
		'i' : COLOR_BLUE, 'j' : COLOR_FUCHSIA, 'k' : COLOR_BLUE, 'l' : COLOR_WHITE, 'm' : COLOR_YELLOW, 'n' : COLOR_RED, 'o' : COLOR_FUCHSIA, 'p' : COLOR_MINT, 'q' : COLOR_FUCHSIA,
		'r' : COLOR_MINT, 's' : COLOR_WHITE, 't' : COLOR_YELLOW, 'u' : COLOR_BLUE, 'v' : COLOR_FUCHSIA, 'w' : COLOR_BLUE,'x' :  COLOR_YELLOW, 'y' : COLOR_RED, 'z' : COLOR_FUCHSIA }

	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	strip.begin()

	def __init__(self):
		pass

	def letters(self, input):
	    return ''.join(filter(str.isalpha, input.lower()))

	def show_word(self, word):

		self.all_off()

		for letter in self.letters(word):
			self.show_letter(letter)

	def show_letter(self, letter):

		position = self.LETTERS[letter] - 1
		color = self.COLORS[letter]

		self.strip.setPixelColor(position, color)
		self.strip.show()	
		time.sleep(1.2)
		self.strip.setPixelColor(position, 0)
		self.strip.show()
		time.sleep(0.7)

	def all_off(self):

		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, 0)

		self.strip.show()

	def random_color_wipe(strip, count=5, groupcount=6, wait_ms=500):

		colors = [ COLOR_BLUE, COLOR_RED, COLOR_YELLOW, COLOR_MINT ]

		for i in range(count):
			start = random.randrange(0, strip.numPixels())

			used_lights = []

			for j in range(groupcount):
				currentPos = start + j
				used_lights.append(currentPos)
				strip.setPixelColor(currentPos, colors[random.randrange(0, 4)])
				strip.show()
				time.sleep(0.2)

			time.sleep(0.5)

			for k in used_lights:
				strip.setPixelColor(k, 0)

			strip.show()
			time.sleep(0.5)



	# Define functions which animate LEDs in various ways.
	def colorWipe(strip, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, 0)
			strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChase(strip, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		for j in range(iterations):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, color)
				strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, 0)

	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256*iterations):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.wheel((i+j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def rainbow_cycle(self, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in range(256*iterations):
			for i in range(self.strip.numPixels()):
				strip.setPixelColor(i, self.wheel((int(i * 256 / strip.numPixels()) + j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChaseRainbow(strip, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, wheel((i+j) % 255))
				strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, 0)
