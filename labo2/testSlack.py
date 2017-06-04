#!/usr/bin/python

from slackclient import SlackClient
token = "token"
sc = SlackClient(token)
resp = sc.api_call(
        "chat.postMessage",
        channel="@ski",
        text="Posting from Script"
)
