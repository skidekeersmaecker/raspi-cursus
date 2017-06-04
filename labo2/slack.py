#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
import socket

token = 'token'
tokendecode = token.decode('utf8')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('gmail.com',80))
sc = SlackClient(tokendecode)
resp = sc.api_call(
       'chat.postMessage',
        channel='@ski',
        text='IP Raspberry ski wifi: ' + s.getsockname()[0]
)

print(resp)
s.close()
