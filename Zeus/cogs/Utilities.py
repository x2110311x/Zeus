import discord

from discord.ext import commands

from .. import exceptions
from ..utilities import Utilities

class cUtilities(commands.Cog, name="Utility Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        msgResp = await ctx.send("Ping?")
        latency = Utilities.msdiff(ctx.message.created_at, msgResp.created_at)
        if latency < 100:
            pingEmbed = discord.Embed(color=0x00ff59)
        elif latency < 200:
            pingEmbed = discord.Embed(color=0xffa600)
        else:
            pingEmbed = discord.Embed(color=0xdb0f00)
        pingEmbed.add_field(name="API Heartbeat", value=f"{int(1000*self.bot.latency)}ms", inline = False)
        pingEmbed.add_field(name="Bot Latency", value=f"{latency}ms", inline = False)
        await msgResp.delete()
        await ctx.send(embed=pingEmbed)

    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("Bot is shutting down")
        raise exceptions.ShutdownSignal
    
def setup(bot):
    bot.add_cog(cUtilities(bot))