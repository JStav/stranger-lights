import tweepy
import time
import stranger_lights

SLEEP_COOLDOWN = 4
COMMAND_ALLOW = '!allow'
COMMAND_RAINBOW = '!rb'
COMMAND_WIPEB = '!wipeb'
COMMAND_WIPEY = '!wipey'
COMMAND_WIPEW = '!wipew'
COMMAND_WIPER = '!wiper'
COMMAND_WIPEF = '!wipef'
COMMAND_WIPEM = '!wipem'

COLOR_BLUE = Color(14, 63, 180)
COLOR_YELLOW = Color(255, 174, 0)
COLOR_WHITE = Color(255, 255, 255)
COLOR_RED = Color(255, 0, 0)
COLOR_FUCHSIA = Color(149, 12, 141)
COLOR_MINT = Color(59, 208, 216)

COMMANDS = { COMMAND_ALLOW, COMMAND_RAINBOW }

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
	elif command == COMMAND_WIPEB:
		driver.color_wipe(COLOR_BLUE)
	elif command == COMMAND_WIPEY:
		driver.color_wipe(COLOR_YELLOW)
	elif command == COMMAND_WIPEW:
		driver.color_wipe(COLOR_WHITE)
	elif command == COMMAND_WIPER:
		driver.color_wipe(COLOR_BLUE)
	elif command == COMMAND_WIPEF:
		driver.color_wipe(COLOR_FUCHSIA)
	elif command == COMMAND_WIPEM:
		driver.color_wipe(COLOR_MINT)
	elif command == COMMAND_ALLOW:
		pass


def parse_message(message):

	global last_id

	# Do nothing if there is no new messages
	if message.id == last_id:
		return

	last_id = message.id
	
	if message.text[0] == '!':
		parse_command(message.text.encode("ascii", "ignore").lower())
	else:
		print message.id
		print message.text
		driver.show_word(message.text.encode("ascii", "ignore"))


while True:

	# Only get the latest message
	messages = api.direct_messages(count=1)


	for message in messages:
		parse_message(message)
	
	time.sleep(SLEEP_COOLDOWN)



