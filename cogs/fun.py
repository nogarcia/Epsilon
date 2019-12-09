"""
Fun cog for Epsilon. Holds all fun commands.
"""

import json
from random import randint
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import html


class XKCD(object):
    def __init__(self, num):
        latest_comic = requests.get("http://xkcd.com/info.0.json").json()
        latest_num = latest_comic["num"]
        if num == 0:
            comic = requests.get(
                "http://xkcd.com/{}/info.0.json".format(randint(1, latest_num))
            ).json()
        elif num > 0:
            comic = requests.get("http://xkcd.com/{}/info.0.json".format(num)).json()
        else:
            comic = latest_comic

        self.url = comic["img"]
        self.alt = comic["alt"]


class ICNDB(object):
    def __init__(self, include, exclude):
        exclude_string = ",".join([str(x) for x in exclude])

        url = "http://api.icndb.com/jokes/random?exclude=[{}]".format(exclude_string)

        if len(include) > 0:
            include_string = ",".join([str(x) for x in include])
            url += "&limitTo=[{}]".format(include_string)

        joke_response = requests.get(url).json()
        if joke_response["type"] == "success":
            self.id = joke_response["value"]["id"]
            self.joke = html.unescape(joke_response["value"]["joke"])
            self.error = False
        elif joke_response["type"] == "NoSuchCategoryException":
            self.id = None
            self.joke = None
            self.error = True
            raise Exception("No such category of ICNDB joke")


class FunCog(commands.Cog):
    """
    Fun cog.
    """

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command()
    async def xkcd(self, ctx, *, comic_id: int = 0):
        """
        Get an xkcd comic in an embed. Returns a random comic unless you give a number.
        """
        comic = XKCD(comic_id)

        if comic.url is None:
            return
        embed = discord.Embed(title="xkcd", color=0x000000)
        embed.set_image(url=comic.url)
        embed.add_field(name="Text", value=comic.alt, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def kaomoji(self, ctx, *, kaomote: str = None):
        """
        Print a kaomoji.
        """
        if kaomote is None or len(kaomote) == 0:
            error_embed = discord.Embed(title="Error", color=0xFF0000, type="rich")
            kaomojis = ", ".join([str(x) for x in self.config["kaomoji"]["kaomotes"]])
            error_embed.add_field(
                name="No kaomoji provided.",
                value="Choose between one of the following: " + kaomojis,
                inline=True,
            )
            await ctx.send(embed=error_embed)
            return
        # Ensure markdown characters are escaped. "
        # "._____." will show up as "._." with italics without escape characters.
        try:
            config_kaomote = self.config["kaomoji"]["kaomotes"][kaomote]
            await ctx.send(config_kaomote)
        except KeyError:
            error_embed = discord.Embed(title="Error", color=0xFF0000, type="rich")
            kaomojis = ", ".join([str(x) for x in self.config["kaomoji"]["kaomotes"]])
            error_embed.add_field(
                name="No kaomoji found.",
                value="Choose between one of the following: " + kaomojis,
                inline=True,
            )
            await ctx.send(embed=error_embed)

    @commands.command()
    async def lyrics(self, ctx, *, song: str = None):
        """
        Get lyrics for a song.
        Song must be in the format of '{artist} {song}'.
        Currently this isn't very accurate (direct URL call, not a search) and will likely give a 404.
        """
        if song is None or len(song) == 0:
            return

        song_url = "https://genius.com/{}-lyrics".format(song.replace(" ", "-").lower())

        page = requests.get(song_url)
        html = BeautifulSoup(page.text, "html.parser")
        song_lyrics = html.find("div", class_="lyrics").get_text()

        if len(song_lyrics) <= 1024:
            await ctx.send(song_lyrics)
        else:
            chunks = [
                song_lyrics[i : i + 1024] for i in range(0, len(song_lyrics), 1024)
            ]
            for chunk in chunks:
                await ctx.send(chunk)

    @commands.command()
    async def icndb(self, ctx):
        """
        Get a joke from the ICNDB (Internet Chuck Norris Database).
        """
        include = self.config["icndb"]["include"]
        exclude = self.config["icndb"]["exclude"]

        joke = ICNDB(include, exclude)

        if not joke.error:
            await ctx.send("Joke #{}: {}".format(joke.id, joke.joke))
        else:
            await ctx.send("Couldn't get joke.")


def setup(bot):
    with open("config/config.json", "r") as f:
        CONFIG = json.load(f)
    bot.add_cog(FunCog(bot, CONFIG))
