#!/usr/bin/python

from slackclient import SlackClient
token = "xoxp-81194043701-81197297509-191024182226-77338c03a42656fff129e35a59330f38"
sc = SlackClient(token)
resp = sc.api_call(
        "chat.postMessage",
        channel="@ski",
        text="Posting from Script"
)
