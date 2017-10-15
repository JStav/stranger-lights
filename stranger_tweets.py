import tweepy
import time
import stranger_lights

SLEEP_COOLDOWN = 4
COMMAND_ALLOW = '!allow'

COMMANDS = { COMMAND_ALLOW }

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
	pass

def parse_message(message):

	global last_id

	# Do nothing if there is no new messages
	if message.id == last_id:
		return

	last_id = message.id
	
	if message.text[0] == '!':
		parse_command(message.text.encode("ascii", "ignore"))
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



