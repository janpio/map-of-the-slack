import os
import json
from slack_sdk import WebClient
import click

def download_channels():
	client = WebClient(os.environ['SLACK_BOT_TOKEN'])

	conversations = []

	with click.progressbar(length=1000, label="Downloading public Slack channels...") as bar:
		currentConversationsRes = client.conversations_list(limit=1000)

		while currentConversationsRes['response_metadata']['next_cursor'] != '':
			conversations += currentConversationsRes['channels']

			currentConversationsRes = client.conversations_list(limit=1000, cursor=currentConversationsRes['response_metadata']['next_cursor'])
			if currentConversationsRes['response_metadata']['next_cursor'] == '':
				progress = 1
			else:
				progress = float(len(conversations)) / float(len(conversations) + 1000)

			bar.pos = int(progress * 999) + 1
			bar.update(1)
			
	conversations += currentConversationsRes['channels']
	conversations.sort(key=lambda x: x['name'])

	conversations = filter(lambda x: x['is_archived'] == False and not x['name'].startswith('zzz-') and x['num_members'] > 5, conversations)
	conversations = list(conversations)

	channelJson = json.dumps(conversations)

	file = open('json_data/channels.json', 'w', encoding='utf-8')
	file.write(channelJson)

	return conversations
