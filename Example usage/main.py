from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import sys
import os
import configparser
import re
import requests
import make_transactions as mt

configParser = configparser.RawConfigParser()
configFilePath = r'settings.ini'

try:
	configParser.read(configFilePath)
	api_id = int(configParser.get('telegram-settings', 'api_id'))
	api_hash = configParser.get('telegram-settings', 'api_hash')
	chats = configParser.get('options', 'chats')
	from_addr = configParser.get('options', 'from_addr')
	key = configParser.get('options', 'key')
except:
	print ('Fill up the settings.ini properly')
	input('Press ENTER to exit...')
	sys.exit()

# function that returns the entity related to sender 
# sender can be person, group or channel
def get_sender_entity(client, sender_id):
	s = client.get_entity(sender_id)
	return s

# function that returns the token address
def listen_to_chats(chats):
	with TelegramClient('myclient', api_id, api_hash) as client:
		client.start()
		dialogs = client.get_dialogs()
		chat_objects = []
		for chat in chats:
			if chat.isdigit():
				chat_objects.append(get_sender_entity(client, int(chat)))
			else:
				chat_objects.append(get_sender_entity(client, chat))
		# add event handler for new message
		client.add_event_handler(new_message_handler, events.NewMessage(chats = chat_objects))
		client.run_until_disconnected()

# event handler for new message from desired sender
def new_message_handler(event):
	print(event.message.message)
	words = re.search("0x[0-9a-f]{40}", event.message.message.lower()).group(0)
	if words[0:2] == '0x':
		print('Found!')
		mt.send_eth(0.0001, from_addr, words, 30000, 40, key)
		print('Sent!')

if __name__ == '__main__':
	chats = chats.split(',')
	print(chats)
	listen_to_chats(chats)
