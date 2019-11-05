"""
Fun cog for Epsilon. Holds all fun commands.
"""

import json
from random import randint
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
# from helpers import scrap_song_url

class FunCog(commands.Cog):
    """
    Fun cog.
    """
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    def get_xkcd(self, comic_id=0):
        """
        Get URL of an XKCD comic. comic_id defaults to 0, meaning random.
        """
        latest_comic = requests.get("http://xkcd.com/info.0.json").json()
        latest_num = latest_comic["num"]
        if comic_id == 0:
            comic = requests.get(
                "http://xkcd.com/{}/info.0.json".format(randint(1, latest_num))).json()
        elif comic_id > 0:
            comic = requests.get(
                "http://xkcd.com/{}/info.0.json".format(comic_id)).json()
        else:
            comic = latest_comic

        comic_url = comic["img"]
        comic_text = comic["alt"]

        return comic_url, comic_text

    @commands.command()
    async def xkcd(self, ctx, *, comic_id: int = 0):
        """
        Get an xkcd comic in an embed. Returns a random comic unless you give a number.
        """
        comic_url, comic_text = self.get_xkcd(comic_id)
        if comic_url is None:
            return
        embed = discord.Embed(
            title="xkcd", color=0x000000
        )
        embed.set_image(url=comic_url)
        embed.add_field(name="Text", value=comic_text, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def kaomoji(self, ctx, *, kaomote: str = None):
        """
        Print a kaomoji.
        """
        if kaomote is None or len(kaomote) == 0:
            return
        # Ensure markdown characters are escaped. "
        # "._____." will show up as "._." with italics without escape characters.
        config_kaomote = self.config["kaomoji"]["kaomotes"][kaomote]
        if config_kaomote is None:
            return
        await ctx.send(config_kaomote)

    @commands.command()
    async def lyrics(self, ctx, *, song: str = None):
        """
        Get lyrics for a song.
        Song must be in the format of '{artist} {song}'.
        Currently this isn't very accurate (direct URL call, not a search) and will likely give a 404.
        """
        if song is None or len(song) == 0:
            return
        
        song_url = "https://genius.com/{}-lyrics".format(song.replace(' ', '-').lower())
        
        page = requests.get(song_url)
        html = BeautifulSoup(page.text, 'html.parser')
        song_lyrics = html.find('div', class_='lyrics').get_text()

        if len(song_lyrics) <= 1024:
            await ctx.send(song_lyrics)
        else:
            chunks = [song_lyrics[i:i+1024] for i in range(0, len(song_lyrics), 1024)]
            for chunk in chunks:
                await ctx.send(chunk)

def setup(bot):
    with open('config/config.json', 'r') as f:
        CONFIG = json.load(f)
    bot.add_cog(FunCog(bot, CONFIG))