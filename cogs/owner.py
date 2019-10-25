import json
import discord
from discord.ext import commands

class OwnerCog(commands.Cog):
    """
    Owner cog. Only works with bot owner.
    """
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def stop(self, ctx):
        """
        Easy stop command for debugging purposes.
        """
        await ctx.send("Stopping.")
        await self.bot.logout()

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cogs_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cogs_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cogs_reload(self, ctx, *, cog: str = None):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        if cog is None:
            for config_cog in self.config['cogs']:
                try:
                    self.bot.unload_extension(config_cog)
                    self.bot.load_extension(config_cog)
                except Exception as e:
                    await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
                else:
                    await ctx.send('**`SUCCESS loading cog {}`**'.format(config_cog))
                     
        else:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.send('**`SUCCESS`**')

    @commands.command(name='status', hidden=True)
    @commands.is_owner()
    async def status(self, ctx, *, status: str=""):
        if len(status) == 0:
            await ctx.send("Clearing status")
            await self.bot.change_presence()
            return
        await ctx.send("Changing status to {}".format(status))
        await self.bot.change_presence(activity=discord.Game(name=status))

def setup(bot):
    with open('config/config.json', 'r') as f:
        CONFIG = json.load(f)
    bot.add_cog(OwnerCog(bot, CONFIG))