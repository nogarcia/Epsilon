"""
The Epsilon code.
"""
import json
import hashlib
from random import randint
import requests
import discord
from discord.ext import commands
import numexpr

with open('config/config.json', 'r') as f:
    CONFIG = json.load(f)

# config stuff
PREFIX = CONFIG['prefix']
CLIENT = discord.Client()

bot = commands.Bot(command_prefix=PREFIX, description="Gamma's Discord helper.")

if __name__ == '__main__':
    for extension in CONFIG['cogs']:
        bot.load_extension(extension)

    TOKEN = CONFIG['token']
    bot.run(TOKEN)

# bot functions
@bot.event
async def on_ready():
    """
    Callback for when the client is ready
    """

    print('Logged on as {0}!'.format(CLIENT.user))