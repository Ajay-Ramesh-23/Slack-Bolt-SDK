import os
from slack_sdk import WebClient
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

load_dotenv()
flask_app = Flask(__name__)
slack_signing_secret = os.environ.get('SIGNING_SECRET')

slack_events_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', flask_app)

client = WebClient(token= os.environ.get("SLACK_BOT_TOKEN"))
BOT_ID=client.api_call("auth.test")['user_id']

@slack_events_adapter.on("message")
def message(payload):
    print(payload)
    event = payload.get('event', {})
    text = event.get('text')
    user_id = event.get('user')
    channel_id=event.get('channel')
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)

if __name__ == "__main__":
    flask_app.run(port=3000)
