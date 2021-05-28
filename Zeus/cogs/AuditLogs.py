import discord
import time

from datetime import datetime
from discord.ext import commands

from .. import exceptions
from ..utilities import Utilities

class cogAuditLogs(commands.Cog, name="Audit Log Commands"):
    def __init__(self, bot):
        self.bot = bot

    # Message Filtering
    ## - Invites
    ## - Slurs
    ## - Misc
    @commands.Cog.listener()
    async def on_message(self, message):
        pass
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        pass

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        pass
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        pass

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_emojis_update(guild, before, after):
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        pass

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        pass
    
    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        pass

    @commands.check
    async def globally_block_dms(ctx):
        return ctx.guild is not None
    
def setup(bot):
    bot.add_cog(cogAuditLogs(bot))