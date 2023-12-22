import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()


client = WebClient(token= os.environ.get("SLACK_BOT_TOKEN"))

try:
    response = client.chat_postMessage(channel='#random', text="Hello world!")
    print(response)
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}")
    assert isinstance(e.response.status_code, int)
    print(f"Received a response status_code: {e.response.status_code}")
