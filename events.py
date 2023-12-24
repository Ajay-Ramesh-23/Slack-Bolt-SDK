import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

load_dotenv()
flask_app = Flask(__name__)

class WelcomeMessage:

    START_TEXT = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text':('Welcome to this channel! \n\n'
                    '*Get started now*'
                )
        }
    }

    DIVIDER = {'type': 'divider'}

    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
        self.icon_emoji = ":robot_face:"
        self.timestamp = ''
        self.completed = False
    
    def get_message(self):
        return {'ts':self.timestamp,
                'channel':self.channel,
                'username':'Robot',
                'icon_emoji':self.icon_emoji,
                'blocks': [self.START_TEXT, self.DIVIDER, self._get_reaction_task()]
                }
    
    def _get_reaction_task(self):
        checkmark = ':white_check_mark:'
        if not self.completed:
            checkmark = ':white_large_square:'
        text = f'{checkmark} *React to this message*'

        return {'type':'section', 'text':{'type':'mrkdwn', 'text':text}}

class EndMessage:
    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
    
    def get_end_message(self):
        return {'channel':self.channel,
                "attachments": 
                [
                    {
                        "mrkdwn_in": ["text"],
                        "color": "#36a64f",
                        "text": "Thanks for using the Slack Bot :smile:"
                    }
                ]
        }

slack_signing_secret = os.environ.get('SIGNING_SECRET')

slack_events_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', flask_app)

client = WebClient(token= os.environ.get("SLACK_BOT_TOKEN"))
BOT_ID=client.api_call("auth.test")['user_id']

message_count = {}
welcome_messages = {}

@flask_app.route('/message-count', methods=['POST'])
def get_message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count_of_user = message_count.get(user_id, 0)
    client.chat_postMessage(channel=channel_id, text=f"We got the request! Number of messages sent: {message_count_of_user}")
    return Response(), 200

def send_welcome_message(channel, user):
    welcome = WelcomeMessage(channel, user)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    welcome.timestamp = response['ts']

    if channel not in welcome_messages:
        welcome_messages[channel] = {}
    welcome_messages[channel][user] = welcome

def send_end_message(channel, user):
    end = EndMessage(channel, user)
    message = end.get_end_message()
    client.chat_postMessage(**message)

@slack_events_adapter.on("message")
def message(payload):
    event = payload.get('event', {})
    text = event.get('text')
    user_id = event.get('user')
    if user_id != None and BOT_ID != user_id:
        if user_id in message_count:
            message_count[user_id] += 1
        else:
            message_count[user_id] = 1
        if text == 'start':
            send_welcome_message(f'@{user_id}', user_id)
        elif text == 'end':
            send_end_message(f'@{user_id}', user_id)


if __name__ == "__main__":
    flask_app.run(port=3000, debug=True)
