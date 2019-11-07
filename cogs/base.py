"""
Base cog.
"""
import json
import discord
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command()
    async def invite(self, ctx, server: str = None):
        """
        Get an invite to a server.
        """
        with open("config/config.json", "r") as f:
            CONFIG = json.load(f)
        if server is None or len(server) == 0:
            await ctx.send(
                "Pick a server from the following: {}".format(
                    list(CONFIG["invites"].keys())
                )
            )
            return
        try:
            invitelink = CONFIG["invites"][server]["url"]
        except KeyError:
            await ctx.send("Invalid server")
            return
        embed = discord.Embed(
            color=0x7289DA, title="Invite", description="Invite to Discord server."
        )
        embed.add_field(name="Discord Invite Link", value=invitelink, inline=True)
        embed.set_footer(text="Link to {}".format(CONFIG["invites"][server]["name"]))
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        """
        Get information about Epsilon.
        """
        embed = discord.Embed(color=0xA2CD48, title="Info")
        embed.add_field(name="Name", value="Epsilon", inline=True)
        embed.add_field(
            name="Source", value="https://github.com/Shrubhog/Epsilon", inline=True
        )
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/545246297062375424/636630299341619201/chrome_ur4GRsKe2b.png"
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BaseCog(bot))
