import logging

from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

SLACK_BOT_TOKEN=""
SLACK_APP_TOKEN=""
SIGNING_SECRET=""

app = App(token=SLACK_BOT_TOKEN,signing_secret=SIGNING_SECRET)

@app.message("(:wave:|Hello)") 
def say_hello(message, say):
    user = message['user']
    channel = message['channel']
    say(f"Hi there, <@{user}>!", channel=channel)

if __name__ == "__main__":
    app.start(port=2500)
