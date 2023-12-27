import logging

from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

SLACK_BOT_TOKEN="xoxb-6381553238448-6355851374565-WfcWZ58F0x32Y08c4Ac1nS5Q"
SLACK_APP_TOKEN="xapp-1-A06AC460762-6392391457765-7b12cc264abbf47c7c7de143ecc5138c7fc2a811b7ede638c546e62dd6872c4c"
SIGNING_SECRET="71b33e9b8846540f4eefdb2d6d3b45b1"

app = App(token=SLACK_BOT_TOKEN,signing_secret=SIGNING_SECRET)

@app.message("(:wave:|Hello)") 
def say_hello(message, say):
    user = message['user']
    channel = message['channel']
    say(f"Hi there, <@{user}>!", channel=channel)

if __name__ == "__main__":
    app.start(port=2500)
