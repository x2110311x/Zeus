import discord
import time

from datetime import datetime
from discord.ext import commands
from re import search as regex

from .. import exceptions
from ..utilities import Utilities

class cogAuditLogs(commands.Cog, name="Audit Log Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def staff_command(self, message):
        guild = self.bot.get_guild(self.bot.config.serverID)
        staffLog = guild.get_channel(self.bot.config.staffCommands_log_channel)
        embed=discord.Embed(title="Staff Command Used")
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name="User ID", value=message.author.id, inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Command", value=message.content, inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await staffLog.send(embed=embed)

    async def process_slurs(self, message):
        pass
    
    async def process_invites(self, message):
        guild = self.bot.get_guild(self.bot.config.serverID)
        staffRole = guild.get_role(self.bot.config.staffRole)
        if staffRole not in message.author.roles:
            return
        inviteregex = "(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/.+[A-Z0-9a-z]"
        if regex(inviteregex, message.content):
            userWarnembed=discord.Embed(title="Please do not send links to other servers!")
            userWarnembed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            userWarnembed.set_footer(text="© 2021 x2110311x")
            await message.channel.send(embed=userWarnembed, content=message.author.mention, delete_after=5.0)

            inviteLog = guild.get_channel(self.bot.config.invite_log_channel)
            embed=discord.Embed(title="User Sent Invite")
            embed=discord.Embed(title="User Sent Invite")
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
            embed.add_field(name="User ID", value=message.author.id, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Message", value=message.content, inline=False)
            embed.set_footer(text="© 2021 x2110311x")
            await inviteLog.send(embed=embed)

    # Message Filtering
    ## - Invites
    ## - Slurs
    ## - Misc
    @commands.Cog.listener()
    async def on_message(self, message):
        await self.process_slurs(message)
        await self.process_invites(message)
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        guild = self.bot.get_guild(self.bot.config.serverID)
        deleteLog = guild.get_channel(self.bot.config.delete_log_channel)
        embed=discord.Embed(title="Message Deleted", color=0x01b725)
        embed.add_field(name="Channel ID", value=payload.channel_id, inline=False)
        embed.add_field(name="Message ID", value=payload.message_id, inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        if payload.cached_message is not None:
            msg = payload.cached_message
            embed.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url)
            embed.add_field(name="User ID", value=msg.author.id, inline=False)
            embed.add_field(name="Message Text", value=msg.content, inline=False)
        else:
            embed.add_field(name="Message Text", value="*Message was not cached*", inline=False)
        embed.add_field(name="Time Deleted", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)

        await deleteLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        guild = self.bot.get_guild(self.bot.config.serverID)
        editLog = guild.get_channel(self.bot.config.edit_log_channel)
        embed=discord.Embed(title="Message Edited", color=0x01b725)
        embed.add_field(name="Channel ID", value=payload.channel_id, inline=False)
        embed.add_field(name="Message ID", value=payload.message_id, inline=False)
        channel = guild.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        embed.add_field(name="New Message Text", value=msg.content, inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        if payload.cached_message is not None:
            oldmsg = payload.cached_message
            embed.set_author(name=oldmsg.author.display_name, icon_url=oldmsg.author.avatar_url)
            embed.add_field(name="Old Message Text", value=oldmsg.content, inline=False)
        else:
            embed.add_field(name="Old Message Text", value="*Message was not cached*", inline=False)
        embed.add_field(name="Time Edited", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)

        await editLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(self.bot.config.serverID)
        joinLog = guild.get_channel(self.bot.config.join_log_channel)
        previouslyJoined = False # NEED TO CHECK DB
        embed=discord.Embed(title="Member Joined", color=0x01b725)
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        embed.add_field(name="User ID", value=member.id, inline=False)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.add_field(name="Previously Joined The Server", value=previouslyJoined, inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await joinLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(self.bot.config.serverID)
        leaveLog = guild.get_channel(self.bot.config.leave_log_channel)
        embed=discord.Embed(title="Member Left Server", color=0x01b725)
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        embed.add_field(name="User ID", value=member.id, inline=False)
        embed.add_field(name="Time Left", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await leaveLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        guild = self.bot.get_guild(self.bot.config.serverID)
        banLog = guild.get_channel(self.bot.config.ban_log_channel)
        banEntry = await guild.fetch_ban(user.id)
        embed=discord.Embed(title="Member Banned", color=0x01b725)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Time Banned", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        if banEntry.reason != None:
            embed.add_field(name="Ban Reason", value=banEntry.reason, inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await banLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        guild = self.bot.get_guild(self.bot.config.serverID)
        banLog = guild.get_channel(self.bot.config.ban_log_channel)
        banEntry = await guild.fetch_ban(user.id)
        embed=discord.Embed(title="Member Unbanned", color=0x01b725)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Time Unbanned", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await banLog.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = self.bot.get_guild(self.bot.config.serverID)
        staffLog = guild.get_channel(self.bot.config.staffCommands_log_channel)
        embed=discord.Embed(title="Channel Deleted", color=0x01b725)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Channel Name", value=channel.name, inline=True)
        embed.add_field(name="Channel ID", value=channel.id, inline=False)
        embed.add_field(name="Time Deleted", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await staffLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = self.bot.get_guild(self.bot.config.serverID)
        staffLog = guild.get_channel(self.bot.config.staffCommands_log_channel)
        embed=discord.Embed(title="Channel Created", color=0x01b725)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Channel Name", value=channel.name, inline=True)
        embed.add_field(name="Channel ID", value=channel.id, inline=False)
        embed.add_field(name="Time Created", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await staffLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        guild = self.bot.get_guild(self.bot.config.serverID)
        staffLog = guild.get_channel(self.bot.config.staffCommands_log_channel)

        if before.name != after.name:
            embed=discord.Embed(title="Channel Name Changed", color=0x01b725)
            embed.add_field(name="Old Name", value=before.name, inline=False)
        elif before.topic != after.topic:
            embed=discord.Embed(title="Channel Topic Changed", color=0x01b725)
            embed.add_field(name="Old Topic", value=before.topic, inline=False)
            embed.add_field(name="New Topic", value=after.topic, inline=False)
        else:
            embed=discord.Embed(title="Channel Updated", color=0x01b725)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Current Channel Name", value=after.name, inline=True)
        embed.add_field(name="Channel ID", value=after.id, inline=False)
        embed.add_field(name="Time Updated", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await staffLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = self.bot.get_guild(self.bot.config.serverID)
        roleLog = guild.get_channel(self.bot.config.role_log_channel)
        embed=discord.Embed(title="Role Created", color=0x01b725)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Role Name", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=False)
        embed.add_field(name="Time Created", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await roleLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = self.bot.get_guild(self.bot.config.serverID)
        roleLog = guild.get_channel(self.bot.config.role_log_channel)
        embed=discord.Embed(title="Role Deleted", color=0x01b725)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Role Name", value=role.name, inline=True)
        embed.add_field(name="Role ID", value=role.id, inline=False)
        embed.add_field(name="Time Deleted", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await roleLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild = self.bot.get_guild(self.bot.config.serverID)
        roleLog = guild.get_channel(self.bot.config.role_log_channel)

        if before.name != after.name:
            embed=discord.Embed(title="Role Name Changed", color=0x01b725)
            embed.add_field(name="Old Name", value=before.name, inline=False)
        elif before.color != after.color:
            embed=discord.Embed(title="Role color Changed", color=0x01b725)
            embed.add_field(name="Old color", value=before.color, inline=False)
            embed.add_field(name="New color", value=after.color, inline=False)
        else:
            embed=discord.Embed(title="Role Updated", color=0x01b725)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Current Role Name", value=after.name, inline=True)
        embed.add_field(name="Role ID", value=after.id, inline=False)
        embed.add_field(name="Time Updated", value=datetime.now().strftime("%b %d, %Y - %I:%M:%S %P") + " GMT", inline=False)
        embed.set_footer(text="© 2021 x2110311x")
        await roleLog.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_emojis_update(guild, before, after):
        # Run a sequence diff between before and after
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = self.bot.get_guild(self.bot.config.serverID)
        vcLog = guild.get_channel(self.bot.config.vc_log_channel)

        if before.channel is None and after.channel is not None:
            embed=discord.Embed(title="User Joined VC", color=0x01b725)
            embed.add_field(name="Channel ID", value=after.channel.id, infline=False)
            embed.add_field(name="Channel Name", value=after.channel.name, infline=False)
        elif before.channel is not None and after.channel is None:
            embed=discord.Embed(title="User Left VC", color=0x01b725)
            embed.add_field(name="Channel ID", value=before.channel.id, infline=False)
            embed.add_field(name="Channel Name", value=before.channel.name, infline=False)
        elif before.channel is not None and after.chanel is not None and before.channel != after.channel:
            embed=discord.Embed(title="User Moved VC", color=0x01b725)
            embed.add_field(name="Old Channel ID", value=before.channel.id, infline=False)
            embed.add_field(name="Old Channel Name", value=before.channel.name, infline=False)
            embed.add_field(name="New Channel ID", value=after.channel.id, infline=False)
            embed.add_field(name="New Channel Name", value=after.channel.name, infline=False)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text="© 2021 x2110311x")

        await vcLog.send(embed=embed)

    @commands.check
    async def globally_block_dms(ctx):
        return ctx.guild is not None
    
def setup(bot):
    bot.add_cog(cogAuditLogs(bot))