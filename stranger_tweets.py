import tweepy
import time
import stranger_lights

SLEEP_COOLDOWN = 4
COMMAND_ALLOW = '!allow'
COMMAND_RAINBOW = '!rb'
COMMAND_THEATER_CHASE = '!tc'
COMMAND_WIPEB = '!wipeb'
COMMAND_WIPEY = '!wipey'
COMMAND_WIPEW = '!wipew'
COMMAND_WIPER = '!wiper'
COMMAND_WIPEF = '!wipef'
COMMAND_WIPEM = '!wipem'
COMMAND_WIPE = '!wipe'

keys = open('keys.txt', 'r')

# Read keys from file
consumer_key = keys.readline().strip()
consumer_secret = keys.readline().strip()
access_token = keys.readline().strip()
access_token_secret = keys.readline().strip()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Init driver
driver = stranger_lights.LightDriver()

# Init last message
last_id = -1

def parse_command(command):

	if command == COMMAND_RAINBOW:
		driver.rainbow_cycle()
	elif command == COMMAND_WIPE:
		driver.color_wipeb()
		driver.color_wipey()
		driver.color_wipew()
		driver.color_wiper()
		driver.color_wipef()
		driver.color_wipem()
	elif command == COMMAND_WIPEB:
		driver.color_wipeb()
	elif command == COMMAND_WIPEY:
		driver.color_wipey()
	elif command == COMMAND_WIPEW:
		driver.color_wipew()
	elif command == COMMAND_WIPER:
		driver.color_wiper()
	elif command == COMMAND_WIPEF:
		driver.color_wipef()
	elif command == COMMAND_WIPEM:
		driver.color_wipem()
	elif command == COMMAND_THEATER_CHASE:
		driver.theater_chase_rainbow()
	elif command == COMMAND_ALLOW:
		pass


def parse_message(message):

	global last_id

	# Do nothing if there is no new messages
	if message.id == last_id:
		return

	last_id = message.id

	print message.id
	print message.text
	
	if message.text[0] == '!':
		parse_command(message.text.encode("ascii", "ignore").lower())
	else:
		driver.show_word(message.text.encode("ascii", "ignore"))


while True:

	# Only get the latest message
	messages = api.direct_messages(count=1)


	for message in messages:
		parse_message(message)
	
	time.sleep(SLEEP_COOLDOWN)



