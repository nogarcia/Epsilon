"""
Fun cog for Epsilon. Holds all fun commands.
"""

from random import randint
import discord
from discord.ext import commands
import requests


class FunCog(commands.Cog):
    """
    Fun cog.
    """
    def __init__(self, bot):
        self.bot = bot

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
        comic_url, comic_text = self.get_xkcd(comic_id)
        if comic_url is None:
            return
        embed = discord.Embed(
            title="XKCD", color=0x000000
        )
        embed.set_image(url=comic_url)
        embed.add_field(name="Text", value=comic_text, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCog(bot))