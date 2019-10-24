"""
Base cog.
"""
import discord
from discord.ext import commands

class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

def setup(bot):
    bot.add_cog(BaseCog(bot))