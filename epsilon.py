"""
The Epsilon code.
"""
import json
import discord

class EpsilonClient(discord.Client):
    """
    The Epsilon Client class. Holds all the functions.
    """
    async def on_ready(self):
        """
        Callback for when the client is ready
        """

        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        """
        Callback for when a message is sent.
        """

        print('Message from {0.author}: {0.content}'.format(message))

with open('config/config.json', 'r') as f:
    CONFIG = json.load(f)

CLIENT = EpsilonClient()
TOKEN = CONFIG['token']
CLIENT.run(TOKEN)
