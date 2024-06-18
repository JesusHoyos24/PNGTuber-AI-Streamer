import socket

# Authentication and channel details
authenticationToken = "oauth:AUTHENTICATION TOKEN GOES HERE"  # Prefix the token with 'oauth:'
ChannelName = "#LumoLoom"  # Channels are prefixed with '#'
TwitchStreamName = "LumoLoom" # Stream name must be the same
PORT = 6667
Link = 'irc.chat.twitch.tv'

# Create a socket and connect to the Twitch IRC server
s = socket.socket()
s.connect((Link, PORT))

# Send the authentication and join the channel
s.send(f"PASS {authenticationToken}\r\n".encode('utf-8'))
s.send(f"NICK {TwitchStreamName}\r\n".encode('utf-8'))
s.send(f"JOIN {ChannelName}\r\n".encode('utf-8'))

# Simple loop to read messages from the server
def BotReadMessages():
    response = s.recv(2048).decode('utf-8')
    username = response
    if response.startswith('PING'):
        s.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
    elif "PRIVMSG" in response:
        parts = response.split(' ', 3)
        if len(parts) >= 4:
            username = parts[0].split('!')[0][1:]
            message = parts[3][1:]
            NewResponse = (f"{username}: {message}")
            return NewResponse
