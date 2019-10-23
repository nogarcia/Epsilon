"""
The Epsilon code.
"""
import json
import discord

with open('config/config.json', 'r') as f:
    CONFIG = json.load(f)

PREFIX = CONFIG['prefix']
CLIENT = discord.Client()
ROOT = CONFIG['root']

@CLIENT.event
async def on_ready():
    """
    Callback for when the client is ready
    """

    print('Logged on as {0}!'.format(CLIENT.user))

@CLIENT.event
async def on_message(message):
    """
    Callback for when a message is sent.
    """

    if message.author == CLIENT.user:
        # Don't talk to yourself. This can lead to infinite loops.
        return
    if message.content.startswith(PREFIX):
        if message.content[len(PREFIX):].startswith('ping'):
            await message.channel.send('pong!')
        elif message.content.startswith('stop') and message.author.id == ROOT:
            # Only stop for the root user
            await CLIENT.logout

TOKEN = CONFIG['token']
CLIENT.run(TOKEN)
