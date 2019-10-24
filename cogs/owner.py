import discord
from discord.ext import commands

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send("Stopping.")
        await self.bot.logout()

def setup(bot):
    bot.add_cog(OwnerCog(bot))