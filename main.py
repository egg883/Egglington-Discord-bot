import aiohttp
import datetime
import time
import io
import json
import os
import discord
from colorama import Fore
import random
import string
import re
from datetime import datetime, timedelta
import sys
from discord_interactions import *
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, ComponentContext, SlashCommandOptionType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_select, create_select_option
from roblox import Client
import asyncio
import requests
from bs4 import BeautifulSoup
import random
import urllib
import urllib.request
import datetime
import pymongo
import time
from discord import Message
import typing
#////////////////////////////////////////////////////////////////////////// COLOR DEFINING
client1 = Client()
class Colours:
    White = "\x1b[38;2;250;250;250m"
    Magenta = "\x1b[38;2;255;94;255m"
#////////////////////////////////////////////////////////////////////////// CONFIG DEFINING#
with open('config.json', 'r') as f:
    config = json.load(f)
bottoken = config['bot_token']
mongodb = config['economy']['mongodb']
dbname = config['economy']['database-name']
prefix = config['prefix']
deletein = config['deletetime']
botowner = config['ownerid']
ownerrole = config['owner']
adminrole = config['admin']
modrole = config['mod']
botcmds = config['botcmds']
server = config['serverid']
logs = config['logs']
playingstatus = config['status']
playingstatus2 = config['status2']
welc = config['welcome']
nsfwonoroff = config['nsfw_enabled']
#////////////////////////////////////////////////////////////////////////// GENERIC SH*T 
embed_color = 0xfcd005
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = prefix, intents=intents, help_command=None)
cmds = {len(bot.commands)}
version = "1.1.4"
slash = SlashCommand(bot, sync_commands=True)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.members = True
MIN_DATE = datetime.datetime(1970, 1, 1)
githuburl = "https://github.com/egg883/Egglington-Discord-bot"
CHANNEL_ID = config['logs']
allowed_guild_ids = [config['serverid']]
total_members = sum([guild.member_count for guild in bot.guilds])
def restart_bot(): 
  os.execv(sys.executable,sys.argv)
#////////////////////////////////////////////////////////////////////////// EVENT STUFF
def new_splash():
    print(f'{Colours.Magenta}Egglington is now Listening to {len(bot.guilds)} servers')
    print(f"{Colours.Magenta}Egglington's Prefix is /")
    print(f"{Colours.Magenta}Do /help for the help commands")


async def log(embed):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.guild.id not in allowed_guild_ids:
        return

    roles_before = set(before.roles)
    roles_after = set(after.roles)

    added_roles = roles_after - roles_before
    removed_roles = roles_before - roles_after

    if added_roles:
        added_roles_str = ", ".join(role.name for role in added_roles)
        embed = discord.Embed(title="Role Update", description=f"{after.mention} was given the following roles: {added_roles_str}", color=discord.Color.green())
        await log(embed)

    if removed_roles:
        removed_roles_str = ", ".join(role.name for role in removed_roles)
        embed = discord.Embed(title="Role Update", description=f"{after.mention} had the following roles removed: {removed_roles_str}", color=discord.Color.red())
        await log(embed)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(welc)
    if not channel:
        return
    if not channel.permissions_for(member.guild.me).send_messages:
        return
    message = f"Welcome to the server, {member.mention}, Please visit <#1048221792147341342> If you are looking to verify you can do so by going to <#1048222728588636210>"
    await channel.send(message)

@bot.event
async def on_connect():
    title = os.system(f"title Egglington Client v{version}")
    time.sleep(1)
    title
    new_splash()

def Clear():
    os.system('cls')
#//////////////////////////////////////////////////////////////////////////
async def ch_pr():
    await bot.wait_until_ready()
    total = 0
    for guild in bot.guilds:
        total += guild.member_count
    formatted_total = '{:,}'.format(total)
    statuses = [
        f"{playingstatus} || {playingstatus2}",
        f"Listening on {len(bot.guilds)} servers",
        f"Still need help? do /help for more help!",
        f"Total Users: {formatted_total}"
    ]
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(10)

bot.loop.create_task(ch_pr())

@bot.command()
async def clearconsole(ctx):
    allowed_userids = [config['ownerid']]
    if not any (role.id in allowed_userids for role in ctx.author.roles):
        await ctx.send("You are not authorized to use this command.")
        return
    ctx.message.delete()
    Clear()
    new_splash()

@slash.slash(name="help", description="Shows this message.")
async def help(ctx: SlashContext):
    nsfw_enabled = config.get('nsfw_enabled', False)
    if not nsfw_enabled:
        embed = discord.Embed(title="Help Panel", description="This is the Help Panel Below will be commands:", color=discord.Color.blue())
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name="General", value="`/whois`, `/yt`, `/vote`, `/choose`, `/poll`", inline=False)
        embed.add_field(name="Fun", value="`/coinflip`, `/rps`, `/dice`, `/pp`, `/8ball`", inline=False)
        embed.add_field(name="Moderation", value=f"`/kick`, `/ban`, `/unban`, `/purge`, `/mute`, `/unmute`, `/lock`, `/unlock`, `/slowmode`", inline=False)
        embed.add_field(name="Server", value=f"`/role`, `/deleterole`, `/first`, `/spfp`, `/avatar`, `/afk`", inline=False)
        embed.add_field(name="Utility", value=f"`/ping`, `/help`, `/invite`, `/sinfo`, `/whois`, `/info`, `/news`, `/newticket`, `/closeticket`, `/support`, `/uptime`", inline=False)
        embed.add_field(name="Memes", value="`/jail`, `/wasted`, `/horny`, `/lolice`, `/pixel`, `/clyde`, `/trump`", inline=False)
        embed.add_field(name="Roblox", value=f"`/rgame`, `/ruser`, `/routfit`, `{prefix}rvalue`, `/ruserhis`", inline=False)
        embed.add_field(name="Crypto", value="`/btc`, `/eth`, `/sol`, `/ltc`, `/usdt`", inline=False)
        await ctx.send(embed=embed)
        return
    nsfw_enabled1 = config.get('nsfw_enabled', True)
    if nsfw_enabled1:
        embed1 = discord.Embed(title="Help Panel", description="This is the Help Panel Below will be commands:", color=discord.Color.blue())
        embed1.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed1.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
        embed1.timestamp = datetime.datetime.utcnow()
        embed1.add_field(name="General", value="`/whois`, `/yt`, `/vote`, `/choose`, `/poll`", inline=False)
        embed1.add_field(name="Fun", value="`/coinflip`, `/rps`, `/dice`, `/pp`, `/8ball`", inline=False)
        embed1.add_field(name="Moderation", value=f"`/kick`, `/ban`, `/unban`, `/purge`, `/mute`, `/unmute`, `/lock`, `/unlock`, `/slowmode`", inline=False)
        embed1.add_field(name="Server", value=f"`/role`, `/deleterole`, `/first`, `/spfp`, `/avatar`, `/afk`", inline=False)
        embed1.add_field(name="Utility", value=f"`/ping`, `/help`, `/invite`, `/sinfo`, `/whois`, `/info`, `/news`, `/newticket`, `/closeticket`, `/support`, `/uptime`", inline=False)
        embed1.add_field(name="Memes", value="`/jail`, `/wasted`, `/horny`, `/lolice`, `/pixel`, `/clyde`, `/trump`", inline=False)
        embed1.add_field(name="Roblox", value=f"`/rgame`, `/ruser`, `/routfit`, `{prefix}rvalue`, `/ruserhis`", inline=False)
        embed1.add_field(name="Crypto", value="`/btc`, `/eth`, `/sol`, `/ltc`, `/usdt`", inline=False)
        embed1.add_field(name="nsfw", value="`/tentacle`, `/hass`, `/hmidriff`, `/pgif`, `/4k`, `/holo`, `/hboobs`, `/pussy`, `/hthigh`, `/thigh`, `/hentai`", inline=False)
        await ctx.send(embed=embed1)
        return


@slash.slash(name="slowmode", description="Set the slowmode of the channel.")
async def slowmode(ctx: SlashContext, seconds: int):
    allowed_roles = [ownerrole, modrole, adminrole]
    allowed_userids = [botowner]
    if not any(role.id in allowed_roles for role in ctx.author.roles) and ctx.author.id not in allowed_userids:
        await ctx.send("You are not authorized to use this command.")
        return
    if seconds > 21600:
        await ctx.send("You can't set the slowmode to more than 21600 seconds.")
        return
    await ctx.channel.edit(slowmode_delay=seconds)
    embed=discord.Embed(title="Slowmode command", url="https://egg883.xyz", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Slowmode set to:", value=f"{seconds} seconds", inline=False)
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    await ctx.send(embed=embed, delete_after=deletein)

@slash.slash(name="lock", description="Lock the channel.")
@commands.has_permissions(manage_channels=True)
async def lock(ctx: SlashContext):
    allowed_ids = [botowner]
    allowed_roles = [ownerrole, modrole, adminrole]
    if ctx.author.id not in allowed_ids and not any(role.id in [r.id for r in ctx.author.roles] for role in allowed_roles):
        await ctx.send("You are not allowed to use this command.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed=discord.Embed(title="Lock command", url="https://egg883.xyz", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Channel locked", value=f"{ctx.channel.mention}", inline=False)
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    await ctx.send(embed=embed, delete_after=deletein)

@slash.slash(name="unlock", description="Unlock the channel.")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx: SlashContext):
    allowed_ids = [botowner]
    allowed_roles = [ownerrole, modrole, adminrole]
    if ctx.author.id not in allowed_ids and not any(role.id in [r.id for r in ctx.author.roles] for role in allowed_roles):
        await ctx.send("You are not allowed to use this command.")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed=discord.Embed(title="Unlock command", url="https://egg883.xyz", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Channel unlocked", value=f"{ctx.channel.mention}", inline=False)
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    await ctx.send(embed=embed, delete_after=deletein)

@slash.slash(
    name="purge",
    description="Delete a specified number of messages from the channel.",
    options=[
        create_option(
            name="limit",
            description="The number of messages to delete. (1-100)",
            option_type=4,
            required=True
        )
    ]
)
@commands.has_permissions(manage_messages=True)
@commands.has_any_role(ownerrole, modrole, adminrole) 
async def purge(ctx: SlashContext, limit: int):
    await ctx.channel.purge(limit=limit+1)
    embed=discord.Embed(title="Purge command", url="https://egg883.xyz", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Purged", value=f"I have purged {limit} messages.")
    await ctx.send(embed=embed,delete_after=config['deletetime'])

afk_users = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author == bot.user:
        return

    # Check for mentions of AFK users
    for user in message.mentions:
        if user.nick is not None and user.nick.startswith('[AFK]'):
            # Send message with AFK status and custom message (if provided)
            if 'is now AFK' in user.nick:
                afk_message = 'is now AFK'
            else:
                afk_message = user.nick.split(': ')[-1]
            await message.channel.send(f"{message.author.mention} {user.mention} is currently AFK. For {afk_message}")

    # Check for AFK users in message content
    if message.author.nick is not None and message.author.nick.startswith('[AFK]'):
        await message.author.edit(nick=message.author.display_name.replace('[AFK]', ''))
        await message.channel.send(f"{message.author.mention} is back from AFK")
        return

    await bot.process_commands(message)

@slash.slash(name="afk",
             description="Set yourself as AFK with a custom message",
             )
async def afk(ctx: SlashContext):
    if ctx.author.nick is not None and ctx.author.nick.startswith('[AFK]'):
        await ctx.send("You're already AFK!")
        return
    nickname = f"[AFK] {ctx.author.display_name}"
    await ctx.author.edit(nick=nickname)
    await ctx.send(f"{ctx.author.mention} is now AFK.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author == bot.user:
        return

    user = None

    # Check for mentions of AFK users
    for mention in message.mentions:
        if mention.nick is not None and mention.nick.startswith('[AFK]'):
            user = mention
            # Send message with AFK status and custom message (if provided)
            if 'is now AFK' in user.nick:
                afk_message = 'No reason provided'
            else:
                afk_message = user.nick.split(': ')[-1]
            await message.channel.send(f"{message.author.mention} {user.mention} is currently AFK.")
            break

    # Check for AFK users in message content
    if message.author.nick is not None and message.author.nick.startswith('[AFK]'):
        user = message.author
        await user.edit(nick=user.display_name.replace('[AFK]', ''))
        await message.channel.send(f"{user.mention} is back from AFK")

    await bot.process_commands(message)


#useful commands thats not ping or help or invite or serverinfo or userinfo
@slash.slash(name="avatar", description="Get the avatar of a user.")
async def avatar(ctx: SlashContext, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"{member.name}'s avatar", color=0x007bff)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)

@slash.slash(name="mute", 
             description="Mutes a user in the server", 
             options=[
                 create_option(
                     name="member", 
                     description="The member to be muted", 
                     option_type=6, 
                     required=True
                 ),
                 create_option(
                     name="reason", 
                     description="The reason for the mute", 
                     option_type=3, 
                     required=False
                 )
             ])
@commands.has_permissions(manage_messages=True)
@commands.has_any_role(ownerrole, modrole, adminrole) 
async def mute(ctx, member: discord.Member, reason: str = None):
    await ctx.defer()
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed, delete_after=config['deletetime'])
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f"You have been muted from: {guild.name}\nReason: {reason}")

@slash.slash(name="unmute",
             description="Unmute a member.",
             options=[
                 create_option(
                     name="member",
                     description="The member to unmute.",
                     option_type=6,
                     required=True
                 ),
                 create_option(
                     name="reason",
                     description="The reason for unmuting.",
                     option_type=3,
                     required=False
                 )
             ])
@commands.has_permissions(manage_messages=True)
@commands.has_any_role(ownerrole, modrole, adminrole)
async def unmute(ctx: SlashContext, member: discord.Member, reason: str = None):
    await ctx.defer()
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted ", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed,delete_after=config['deletetime'])
    await member.remove_roles(mutedRole, reason=reason)
    await member.send(f" You have been unmuted in: {guild.name} reason: {reason}")

@slash.slash(name="whois",
             description="Shows information about a member.",
             options=[
                 create_option(
                     name="member",
                     description="The member you want to see information about.",
                     option_type=6,
                     required=True
                 )
             ])
async def whois(ctx: SlashContext, member: discord.Member):
    embed = discord.Embed(title=f"Info about **{member.display_name}**", colour=0x007bff)
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"Egglington", url="https://egg883.xyz", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="User ID:", value=f"```{member.id}```", inline=False)
    embed.add_field(name="Users Discriminator:", value=f"```#{member.discriminator}```", inline=True)
    embed.add_field(name="Creation Date:", value=f"```{member.created_at.strftime('%d/%m/%Y')}```", inline=True)
    embed.add_field(name="Server Join Date:", value=f"```{member.joined_at.strftime('%d/%m/%Y')}```", inline=True)
    embed.add_field(name="Is a bot:", value=f"```{member.bot}```", inline=True)
    await ctx.send(embed=embed)
    await ctx.message.delete(delay=deletein)

@slash.slash(name="role",
             description="Gives a specified role to a member",
             options=[
                 create_option(
                     name="member",
                     description="The member to give the role to",
                     option_type=6,
                     required=True
                 ),
                 create_option(
                     name="rname",
                     description="The name of the role to give",
                     option_type=3,
                     required=True
                 )
             ])
@commands.has_permissions(manage_roles=True)
async def give_role(ctx: SlashContext, member: discord.Member, rname: str):
    await ctx.defer()
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=rname)
    if not role:
        role = await guild.create_role(name=rname)
        for channel in guild.channels:
            await channel.set_permissions(role, speak=True, send_messages=True, read_message_history=True, read_messages=True)
        embed = discord.Embed(title="Created Role", colour=0x007bff)
        embed.set_author(name=f"Egglington", url="https://egg883.xyz", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name="Created role:", value=f"The Role: {rname} Has successfully been given to {member.display_name}", inline=False)
    await member.add_roles(role)
    await ctx.send(embed=embed, delete_after=config['deletetime'])

@slash.slash(name="deleterole",
             description="Deletes the specified role",
             options=[
                 create_option(
                     name="role",
                     description="The role to delete",
                     option_type=8,
                     required=True
                 )
             ])
@commands.has_any_role(ownerrole, modrole, adminrole) 
async def _deleterole(ctx: SlashContext, role: discord.Role):
    await ctx.defer()
    if ctx.author.guild_permissions.administrator:
        guild = ctx.guild
        if role in guild.roles:
            await role.delete()
            await ctx.send(f"The role `{role}` has been deleted!", hidden=True)
            return
    await ctx.send("You don't have permission to delete this role or the role doesn't exist!", hidden=True)

@slash.slash(name="pp", description="Check someone's pp size", options=[
    create_option(
        name="user",
        description="The user whose pp size you want to check",
        option_type=6,
        required=False
    )
])
async def pp(ctx: SlashContext, user: discord.Member = None):
    await ctx.defer()
    if user is None:
        user = ctx.author
    size = random.randint(1, 15)
    dong = ""
    for _i in range(0, size):
        dong += "="
    embed = discord.Embed(title=F"PP command executed!", url="https://egg883.xyz", colour=0x007bff)
    embed.set_author(name=f"Egglington", url="https://egg883.xyz", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name=f"{user}'s PP size is: ", value=f"8{dong}D", inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@slash.slash(name="unban",
             description="Unbans a member from the server.",
             options=[
                 create_option(
                     name="member",
                     description="The member you want to unban. You can use either a mention or their user ID.",
                     option_type=3,
                     required=True
                 )
             ])
@commands.has_permissions(ban_members=True)
@commands.has_any_role(1063848147476025456, ownerrole, modrole, adminrole)
async def unban(ctx: SlashContext, member: str):
    await ctx.defer()

    guild = ctx.guild

    try:
        member_obj = await guild.fetch_member(int(member.strip("<@!>")))
        await guild.unban(member_obj)
        embed = discord.Embed(title="Unbanned", description=f"{member_obj.mention} was unbanned", colour=0x007bff)
    except discord.errors.NotFound:
        await guild.unban(discord.Object(id=int(member)))
        embed = discord.Embed(title="Unbanned", description=f"User with ID {member} was unbanned", colour=0x007bff)

    await ctx.send(embed=embed, delete_after=config['deletetime'])

@slash.slash(name="ban",
             description="Bans a member from the server",
             options=[
                 create_option(
                     name="member",
                     description="The member to ban",
                     option_type=6,
                     required=True
                 ),
                 create_option(
                     name="reason",
                     description="The reason for the ban",
                     option_type=3,
                     required=False
                 )
             ])
@commands.has_permissions(ban_members=True)
async def ban(ctx: SlashContext, member: discord.Member, reason: str = None):
    if reason is None:
        reason = "No reason provided"

    await member.ban(reason=reason)

    embed = discord.Embed(
        title="Member banned",
        description=f"{member.mention} has been banned from the server.",
        color=0xFF0000
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Reason", value=reason)

    await ctx.send(embed=embed)

@slash.slash(name="kick",
             description="Kicks a member from the server",
             options=[
                 create_option(
                     name="member",
                     description="The member to kick",
                     option_type=6,
                     required=True
                 ),
                 create_option(
                     name="reason",
                     description="The reason for the kick",
                     option_type=3,
                     required=False
                 )
             ])
@commands.has_permissions(kick_members=True)
async def kick(ctx: SlashContext, member: discord.Member, reason: str = "No reason specified"):
    guild = ctx.guild
    await member.send(f"You have been kicked from {guild.name}. Reason: {reason}")
    await member.kick(reason=reason)
    
    embed = discord.Embed(
        title="Kick Log",
        description=f"{member.mention} has been **kicked** by {ctx.author.mention}.",
        color=0x1355ed
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="User", value=f"{member}", inline=True)
    embed.add_field(name="UserID", value=f"{member.id}", inline=True)
    embed.add_field(name="Reason", value=f"{reason}", inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embeds=[embed])

@slash.slash(name="restart",
             description="Restart the bot"
)
@commands.has_any_role(botowner)
async def restart(ctx: SlashContext):
    await ctx.defer()
    embed=discord.Embed(title="Command Executed", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1072208453323460790/giphy.gif")
    embed.add_field(name="**Please Wait**", value="Bot Is Restarting.", inline=False)
    await ctx.send(embed=embed, delete_after=deletein)
    print("restarting bot")
    restart_bot()


@slash.slash(name="news", description="Displays the latest news about the bot.")
async def news(ctx: SlashContext):
    await ctx.defer()
    embed = discord.Embed(title=f"Update V{version}", description=f"This is the latest news about our bot Update", url=f"{githuburl}", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Added Slash commands", value="```added ticket slash command```", inline=False)
    embed.add_field(name="stupid gay ritem broke", value="```Removed ritem due to issues```", inline=False)
    embed.add_field(name="Our Website", value="```https://egg883.xyz```", inline=False)
    await ctx.send(embed=embed)


@slash.slash(name="sinfo", description="Get information about the server")
async def sinfo(ctx):
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    guild = ctx.guild
    categories = len(ctx.guild.categories)
    member_count = len(ctx.guild.members)
    channels = text_channels + voice_channels
    embed = discord.Embed(title="Server Info", description=f"This is info about **{guild.name}**", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url=f"{guild.icon_url}")
    embed.add_field(name="Server ID", value=f"```{ctx.guild.id}```", inline=False)
    embed.add_field(name="Channel Count", value=f"```{channels} Channels {text_channels} Text, {voice_channels} Voice, {categories}```", inline=False)
    embed.add_field(name="Server Owner", value=f"```{ctx.guild.owner}```", inline=True)
    embed.add_field(name="Member Count", value=f"```{member_count}```", inline=True)
    embed.add_field(name="Server Verification", value=f"```{str(ctx.guild.verification_level).upper()}```", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="info", description="Displays info about the bot.")
async def info(ctx):
    embed = discord.Embed(title="Info", description=f"This is a information page about my bot", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Total Commands:", value = f"```{len(slash.commands)}```", inline=True)
    embed.add_field(name="Prefix:", value=f"```{prefix}```", inline=True)
    embed.add_field(name="Version:", value=f"```{version}```", inline=True)
    embed.add_field(name="Creator:", value="```This bot was made by jackk#6666 this is a little project i wanted todo```", inline=False)
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="first", description="Displays the first message ever sent in the channel.")
async def first(ctx):
    await ctx.defer()
    channel = ctx.channel
    first_message = (await channel.history(limit = 1, oldest_first = True).flatten())[0]
    embed = discord.Embed(title="First message", description=f"This is the first ever message sent in this channel", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="First Message Content", value = f"{first_message.content}", inline=False)
    embed.add_field(name="First Message link", value = f"{first_message.jump_url}", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="spfp", description="Displays the server icon.")
async def spfp(ctx):
    await ctx.defer()
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}'s Server Icon", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_image(url=f"{guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    await ctx.send(embed=embed, delete_after=deletein)

@slash.slash(name="jail", 
             description="Send someone to jail!",
             options=[
                 create_option(
                     name="member",
                     description="The member you want to send to jail.",
                     option_type=SlashCommandOptionType.USER,
                     required=False
                 )
             ])
async def jail(ctx: SlashContext, member: typing.Optional[discord.Member] = None):
    if member is None:
        member = ctx.author
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read())
            await trigSession.close()
            await ctx.send(file=discord.File(imageData, 'eggui.gif'))


@slash.slash(name="ruser",
             description="Get information about a Roblox user.",
             options=[
                 create_option(
                     name="username",
                     description="The Roblox username of the user.",
                     option_type=3,
                     required=True
                 )
             ])
async def ruser(ctx, username):
    user = await client1.get_user_by_username(username)
    userid = user.id
    URL3 = f"https://www.roblox.com/users/{userid}/profile"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    listofusers = requests.get(f'https://www.rolimons.com/playerapi/player/{userid}').json()
    user_thumbnails = await client1.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        size=(420, 420)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        followers = soup.find('div', class_="hidden")["data-followerscount"]
        following = soup.find('div', class_="hidden")["data-followingscount"]
        friends = soup.find('div', class_="hidden")["data-friendscount"]
        placevisits = soup.find('div', class_="text-lead text-overflow slide-item-my-rank games").text
        embed=discord.Embed(title=f"Found Info for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_thumbnail(url=f"{user_thumbnail.image_url}")
        embed.add_field(name=f"Display name:", value=f"```{user.display_name}```", inline=False)
        embed.add_field(name=f"User ID:", value=f"```{user.id}```", inline=True)
        embed.add_field(name=f"Friends:", value=f"```{friends}```", inline=True)
        embed.add_field(name=f"Followers:", value=f"```{followers}```", inline=True)
        embed.add_field(name=f"Following:", value=f"```{following}```", inline=True)
        embed.add_field(name=f"Place Visits:", value=f"```{placevisits}```", inline=True)
        embed.add_field(name=f"Creation Date:", value=f"```{user.created.strftime('%Y')}```", inline=True)
        embed.add_field(name=f"Premium:", value=f"```{listofusers['premium']}```", inline=True)
        embed.add_field(name=f"Is banned:", value=f"```{user.is_banned}```", inline=True)
        embed.add_field(name=f"Description:", value=f"```{user.description}```", inline=False)
        embed.set_footer(text=f"{username}'s Information", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(
    name="routfit",
    description="Find the current outfit of a Roblox user",
    options=[
        create_option(
            name="username",
            description="The username of the Roblox user",
            option_type=3,
            required=True
        )
    ]
)
async def routfit(ctx: SlashContext, username: str):
    user = await client1.get_user_by_username(username)
    user_thumbnails = await client1.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        size=(420, 420)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        embed=discord.Embed(title=f"Found current outfit for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name=f"Username:", value=f"{user.name}", inline=False)
        embed.set_image(url = f"{user_thumbnail.image_url}")
        embed.set_footer(text=f"{username}'s current outfit", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="wasted",
             description="Apply the GTA 'Wasted' effect to a user's avatar",
             options=[
                 create_option(
                     name="user",
                     description="The user to apply the effect to (optional, defaults to yourself)",
                     option_type=6,
                     required=False
                 )
             ])
async def wasted(ctx, user: discord.Member = None):
    await ctx.defer()
    if user is None:
        user = ctx.author
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://some-random-api.ml/canvas/wasted?avatar={user.avatar_url_as(format='png', size=1024)}") as resp:
            if resp.status == 200:
                img_bytes = io.BytesIO(await resp.read())
                file = discord.File(img_bytes, filename="wasted.gif")
                await ctx.send(file=file)
            else:
                await ctx.send("An error occurred while processing the command.")


@slash.slash(name="youtube",
             description="Searches YouTube for a video.",
             options=[
                 create_option(
                     name="search",
                     description="The search query for the YouTube video.",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 )
             ])
async def _youtube(ctx: SlashContext, search: str):
    author = ctx.author
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_content = html_content.read().decode()
    search_results = re.findall(r'\/watch\?v=\w+', search_content)
    await ctx.send(f'{author.mention} result for {search}:\n https://www.youtube.com' + search_results[0])

@slash.slash(name="lolice",
             description="Generates a lolice image with the avatar of the specified member or yourself",
             options=[
                 create_option(
                     name="member",
                     description="The member to generate the image for. If not specified, the command user will be used",
                     option_type=6,
                     required=False
                 )
             ])
async def lolice(ctx: SlashContext, member: typing.Optional[discord.Member] = None):
    await ctx.defer()
    if member is None:
        member = ctx.author
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/lolice?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read())
        await trigSession.close()
        await ctx.send(file=discord.File(imageData, 'eggui.gif'))

@slash.slash(name="trump",
             description="Generate a fake tweet from Donald Trump with your message.")
async def _trump(ctx, msg: str):
    response = requests.get(f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={msg}")
    stuff = json.loads(response.text)
    embed = discord.Embed(title="Meanwhile on twitter:",
                          color=0x007bff)
    embed.set_author(name="Egglington",
                     url="https://egg883.xyz",
                     icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz",
                     icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_image(url=stuff['message'])
    await ctx.send(embed=embed)

@slash.slash(name="horny", description="Generates a horny image with the user's avatar or the mentioned user's avatar", options=[
    create_option(
        name="user",
        description="The user to generate the image for",
        option_type=6,
        required=False
    )
])
async def _horny(ctx: SlashContext, user: discord.Member = None):
    await ctx.defer(hidden=True)
    if user is None:
        user = ctx.author
    else:
        user = ctx.guild.get_member(user.id)
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/horny?avatar={user.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read())
            await trigSession.close()
            await ctx.send(file=discord.File(imageData, 'eggui.gif'))

@slash.slash(name="clyde",
             description="Make Clyde say something",
             options=[
                 create_option(
                     name="msg",
                     description="The message Clyde should say",
                     option_type=3,
                     required=True
                 )
             ])
async def clyde(ctx: SlashContext, msg: str):
    await ctx.defer()
    response = requests.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={msg}")
    stuff = json.loads(response.text)
    embed=discord.Embed(title="Clyde has a message for you", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_image(url = stuff['message'])
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="pixel",
             description="Pixelate a user's avatar",
             options=[
                 create_option(
                     name="member",
                     description="The user whose avatar to pixelate",
                     option_type=6,
                     required=False
                 )
             ])
async def pixel(ctx: SlashContext, member: discord.Member = None):
    await ctx.defer()
    if member is None:
        member = ctx.author
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format="png", size=1024)}') as img:
            image_data = io.BytesIO(await img.read())
            await session.close()
            await ctx.send(file=discord.File(image_data, 'eggui.gif'))

@slash.slash(name="nsfw", description="NSFW commands", options=[
    create_option(
        name="category",
        description="Category name",
        option_type=3,
        required=False,
        choices=[
            create_choice(name="tentacle", value="tentacle"),
            create_choice(name="hass", value="hass"),
            create_choice(name="hmidriff", value="hmidriff"),
            create_choice(name="pgif", value="pgif"),
            create_choice(name="4k", value="4k"),
            create_choice(name="holo", value="holo"),
            create_choice(name="hboobs", value="hboobs"),
            create_choice(name="pussy", value="pussy"),
            create_choice(name="hthigh", value="hthigh"),
            create_choice(name="thigh", value="thigh"),
            create_choice(name="hentai", value="hentai")
        ]
    )
])
async def nsfw(ctx: SlashContext, category: str = None):
    nsfw_enabled = config.get('nsfw_enabled', False)
    if not nsfw_enabled:
        await ctx.send("NSFW commands are disabled.")
        return
    if not ctx.channel.is_nsfw():
        await ctx.send("This command can only be used in NSFW channels.")
        return
    await ctx.defer()
    if category is None:
        embed=discord.Embed(title="NSFW Commands", description = "**THESE MUST BE SENT IN AN NSFW CHANNEL**", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name="NSFW Command Usage", value = f"/nsfw (category name)", inline=False)
        embed.add_field(name="**NSFW Categories**", value=f"tentacle\nhass\nhmidriff\npgif\n4k\nholo\nhboobs\npussy\nhthigh\nthigh\nhentai", inline=True)
        await ctx.send(embed=embed, delete_after=deletein)

    elif category.lower() == "tentacle":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=tentacle')
        res = r.json()
        embed=discord.Embed(title="Tentacle", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif category.lower() == "hass":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=hass')
        res = r.json()
        embed=discord.Embed(title="Hentai Ass", color=0x007bff)
        embed.set_author(name ="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif category.lower() == "hmidriff":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=hmidriff')
        res = r.json()
        embed=discord.Embed(title="Hentai Midriff", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
    elif category.lower() == "pgif":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=pgif')
        res = r.json()
        embed=discord.Embed(title="Porn Gif", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
    elif category.lower() == "4k":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=4k')
        res = r.json()
        embed=discord.Embed(title="4K Porn", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
    elif category.lower() == "holo":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=holo')
        res = r.json()
        embed=discord.Embed(title="Holo", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
    elif category.lower() == "hentai":
        r = requests.get(f'https://nekobot.xyz/api/image?type=hentai')
        res = r.json()
        embed=discord.Embed(title="Hentai", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
    elif category.lower() == "tits":
        r = requests.get(f'https://nekobot.xyz/api/image?type=tits')
        res = r.json()
        embed=discord.Embed(title="Tits", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
    elif category.lower() == "waifu":
        r = requests.get(f'https://nekobot.xyz/api/image?type=waifu')
        res = r.json()
        embed=discord.Embed(title="Waifu", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
    else:
        await ctx.send(f"Sorry {ctx.author.mention}, I couldn't find any results for that category. Please use one of the following categories: anal, ass, boobs, hentai, hmidriff, pgif, 4k, holo, tits, waifu.")






@slash.slash(name="ruserhis",
             description="Gets Roblox user's past usernames.",
             options=[
                 create_option(
                     name="username",
                     description="The Roblox username of the user.",
                     option_type=3,
                     required=True
                 )
             ])
async def ruserhis(ctx,username):
    user = await client1.get_user_by_username(username)
    userid = user.id
    URL3 = f"https://www.roblox.com/users/{userid}/profile"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    user_thumbnails = await client1.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        size=(420, 420)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        users = soup.find('span',  class_="tooltip-pastnames")['title']
        embed=discord.Embed(title=f"Past usernames for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_thumbnail(url=f"{user_thumbnail.image_url}")
        embed.add_field(name=f"Past usernames", value=f"```{users}```", inline=False)
        embed.set_footer(text=f"{username}'s Past Usernames", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@bot.command()
async def rvalue(ctx, username):
    user = await client1.get_user_by_username(username)
    userid = str(user.id)
    listofusers1 = requests.get(f'https://www.rolimons.com/playerapi/player/{userid}').json()
    user_thumbnails = await client1.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        size=(420, 420)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        URL = f"https://www.rolimons.com/player/{userid}"
    requestURL = requests.get(URL)
    content = requestURL.content
    URL3 = f"https://www.rolimons.com/player/{userid}"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup1 = BeautifulSoup(content, "html.parser")
    URL3 = f"https://rblx.trade/u/{username}"
    requestURL = requests.get(URL3)
    content = requestURL.content
    trade = soup1.find('span',class_="card-title mb-1 text-light stat-data text-nowrap").text
    count = 0
    url = f"https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?limit=100&sortOrder=Asc"

    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        count += len(data['data'])

        try:
            while data['nextPageCursor'] != "null":
                url = f"https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?limit=100&sortOrder=Asc&cursor={data['nextPageCursor']}"
                with urllib.request.urlopen(url) as url:
                    data = json.loads(url.read().decode())
                    count += len(data['data'])
        except:
            pass
    embed=discord.Embed(title=f"Rolimons Info for {user.name} ", url=f"https://www.rolimons.com/player/{userid}", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url=f"{user_thumbnail.image_url}")
    embed.add_field(name=f"Username:", value=f"```{listofusers1['name']}```", inline=True)
    embed.add_field(name=f"Rank:", value=f"```{listofusers1['rank']}```", inline=True)
    embed.add_field(name=f"RAP:", value=f"```{listofusers1['rap']}```", inline=True)
    embed.add_field(name=f"Value:", value=f"```{listofusers1['value']}```", inline=True)
    embed.add_field(name=f"Collectables:", value=f"```{count}```", inline=True)
    embed.add_field(name=f"Trade ads:", value=f"```{trade}```", inline=True)
    embed.add_field(name=f"Premium:", value=f"```{listofusers1['premium']}```", inline=True)
    embed.add_field(name=f"Terminated:", value=f"```{listofusers1['terminated']}```", inline=True)
    embed.add_field(name=f"Private:", value=f"```{listofusers1['privacy_enabled']}```", inline=True)
    embed.add_field(name=f"Last Location:", value=f"```{listofusers1['last_location']}```", inline=True)
    embed.set_footer(text=f"{username}'s rolimons", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1079482029776842812/JCiYruAM_400x400.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="BTC",
             description="Get the current price of Bitcoin.")
async def _btc(ctx):
    URL3 = f"https://coinmarketcap.com/currencies/bitcoin/"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    URL4 = "https://www.coindesk.com/price/bitcoin/"
    requestURL = requests.get(URL4)
    content = requestURL.content
    soup1 = BeautifulSoup(content, "html.parser")
    acronym = soup.find('small').text
    price = soup.find('div', class_="priceValue").text
    rank = soup.find('div', class_="namePill namePillPrimary").text
    market = soup.find('div', class_="statsValue").text
    vol = soup.find_all('div', class_="statsValue")[2].text
    percent = soup1.find('h6', class_="typography__StyledTypography-owin6q-0 hZxwDe").text
    highest = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[4].text
    Rytd = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[5].text
    fee = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[11].text
    embed=discord.Embed(title=f"Information about Bitcoin", url=f"https://coinmarketcap.com/currencies/bitcoin/", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name=f"Name:", value=f"```Bitcoin```", inline=True)
    embed.add_field(name=f"Acronym:", value=f"```{acronym}```", inline=True)
    embed.add_field(name=f"Market Rank:", value=f"```{rank}```", inline=True)
    embed.add_field(name=f"Price:", value=f"```{price}```", inline=True)
    embed.add_field(name=f"Market Cap:", value=f"```{market}```", inline=True)
    embed.add_field(name=f"Volume [24hrs]:", value=f"```{vol}```", inline=True)
    embed.add_field(name=f"Percent [24hrs]:", value=f"```{percent}```", inline=True)
    embed.add_field(name=f"Highest AllTime:", value=f"```{highest}```", inline=True)
    embed.add_field(name=f"Return YTD:", value=f"```{Rytd}```", inline=True)
    embed.add_field(name=f"Average Fee [24hrs]:", value=f"```{fee}```", inline=True)
    embed.set_footer(text=f"bitcoin's info", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1086238157693001788/bitcoin-logo-5234.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="ETH",
             description="Get information about Ethereum")
async def _eth(ctx):
    URL3 = f"https://coinmarketcap.com/currencies/Ethereum/"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    URL4 = "https://www.coindesk.com/price/Ethereum/"
    requestURL = requests.get(URL4)
    content = requestURL.content
    soup1 = BeautifulSoup(content, "html.parser")
    acronym = soup.find('small').text
    price = soup.find('div', class_="priceValue").text
    rank = soup.find('div', class_="namePill namePillPrimary").text
    market = soup.find('div', class_="statsValue").text
    vol = soup.find_all('div', class_="statsValue")[2].text
    percent = soup1.find('h6', class_="typography__StyledTypography-owin6q-0 hZxwDe").text
    highest = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[4].text
    Rytd = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[5].text
    fee = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[11].text
    name = soup.find('span', class_="sc-1d5226ca-1 fLa-dNu").text
    embed=discord.Embed(title=f"Information about {name}", url=f"https://coinmarketcap.com/currencies/Ethereum/", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name=f"Name:", value=f"```{name}```", inline=True)
    embed.add_field(name=f"Acronym:", value=f"```{acronym}```", inline=True)
    embed.add_field(name=f"Market Rank:", value=f"```{rank}```", inline=True)
    embed.add_field(name=f"Price:", value=f"```{price}```", inline=True)
    embed.add_field(name=f"Market Cap:", value=f"```{market}```", inline=True)
    embed.add_field(name=f"Volume [24hrs]:", value=f"```{vol}```", inline=True)
    embed.add_field(name=f"Percent [24hrs]:", value=f"```{percent}```", inline=True)
    embed.add_field(name=f"Highest AllTime:", value=f"```{highest}```", inline=True)
    embed.add_field(name=f"Return YTD:", value=f"```{Rytd}```", inline=True)
    embed.add_field(name=f"Average Fee [24hrs]:", value=f"```{fee}```", inline=True)
    embed.set_footer(text=f"{name}'s info", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="sol",
             description="Get information about Solana")
async def _sol(ctx):
    URL3 = f"https://coinmarketcap.com/currencies/solana/"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    URL4 = "https://www.coindesk.com/price/solana/"
    requestURL = requests.get(URL4)
    content = requestURL.content
    soup1 = BeautifulSoup(content, "html.parser")
    acronym = soup.find('small').text
    price = soup.find('div', class_="priceValue").text
    rank = soup.find('div', class_="namePill namePillPrimary").text
    market = soup.find('div', class_="statsValue").text
    vol = soup.find_all('div', class_="statsValue")[2].text
    percent = soup1.find('h6', class_="typography__StyledTypography-owin6q-0 hZxwDe").text
    highest = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[4].text
    Rytd = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[5].text
    fee = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[11].text
    name = soup.find('span', class_="sc-1d5226ca-1 fLa-dNu").text
    embed=discord.Embed(title=f"Information about {name}", url=f"https://coinmarketcap.com/currencies/solana/", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name=f"Name:", value=f"```{name}```", inline=True)
    embed.add_field(name=f"Acronym:", value=f"```{acronym}```", inline=True)
    embed.add_field(name=f"Market Rank:", value=f"```{rank}```", inline=True)
    embed.add_field(name=f"Price:", value=f"```{price}```", inline=True)
    embed.add_field(name=f"Market Cap:", value=f"```{market}```", inline=True)
    embed.add_field(name=f"Volume [24hrs]:", value=f"```{vol}```", inline=True)
    embed.add_field(name=f"Percent [24hrs]:", value=f"```{percent}```", inline=True)
    embed.add_field(name=f"Highest AllTime:", value=f"```{highest}```", inline=True)
    embed.add_field(name=f"Return YTD:", value=f"```{Rytd}```", inline=True)
    embed.add_field(name=f"Average Fee [24hrs]:", value=f"```{fee}```", inline=True)
    embed.set_footer(text=f"{name}'s info", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="USDT",
             description="Display information about Tether (USDT).")
async def _tether(ctx):
    URL3 = f"https://coinmarketcap.com/currencies/tether/"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    URL4 = "https://www.coindesk.com/price/tether/"
    requestURL = requests.get(URL4)
    content = requestURL.content
    soup1 = BeautifulSoup(content, "html.parser")
    acronym = soup.find('small').text
    price = soup.find('div', class_="priceValue").text
    rank = soup.find('div', class_="namePill namePillPrimary").text
    market = soup.find('div', class_="statsValue").text
    vol = soup.find_all('div', class_="statsValue")[2].text
    percent = soup1.find('h6', class_="typography__StyledTypography-owin6q-0 hZxwDe").text
    highest = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[4].text
    Rytd = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[5].text
    fee = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[11].text
    name = soup.find('span', class_="sc-1d5226ca-1 fLa-dNu").text
    embed=discord.Embed(title=f"Information about {name}", url=f"https://coinmarketcap.com/currencies/tether/", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name=f"Name:", value=f"```{name}```", inline=True)
    embed.add_field(name=f"Acronym:", value=f"```{acronym}```", inline=True)
    embed.add_field(name=f"Market Rank:", value=f"```{rank}```", inline=True)
    embed.add_field(name=f"Price:", value=f"```{price}```", inline=True)
    embed.add_field(name=f"Market Cap:", value=f"```{market}```", inline=True)
    embed.add_field(name=f"Volume [24hrs]:", value=f"```{vol}```", inline=True)
    embed.add_field(name=f"Percent [24hrs]:", value=f"```{percent}```", inline=True)
    embed.add_field(name=f"Highest AllTime:", value=f"```{highest}```", inline=True)
    embed.add_field(name=f"Return YTD:", value=f"```{Rytd}```", inline=True)
    embed.add_field(name=f"Average Fee [24hrs]:", value=f"```{fee}```", inline=True)
    embed.set_footer(text=f"{name}'s info", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="LTC",
             description="Display information about Litecoin (LTC).")
async def _litecoin(ctx):
    URL3 = f"https://coinmarketcap.com/currencies/litecoin/"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    URL4 = "https://www.coindesk.com/price/litecoin/"
    requestURL = requests.get(URL4)
    content = requestURL.content
    soup1 = BeautifulSoup(content, "html.parser")
    acronym = soup.find('small').text
    price = soup.find('div', class_="priceValue").text
    rank = soup.find('div', class_="namePill namePillPrimary").text
    market = soup.find('div', class_="statsValue").text
    vol = soup.find_all('div', class_="statsValue")[2].text
    percent = soup1.find('h6', class_="typography__StyledTypography-owin6q-0 hZxwDe").text
    highest = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[4].text
    Rytd = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[5].text
    fee = soup1.find_all('span', class_="typography__StyledTypography-owin6q-0 gaZnSf")[11].text
    name = soup.find('span', class_="sc-1d5226ca-1 fLa-dNu").text
    embed=discord.Embed(title=f"Information about {name}", url=f"https://coinmarketcap.com/currencies/litecoin/", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name=f"Name:", value=f"```{name}```", inline=True)
    embed.add_field(name=f"Acronym:", value=f"```{acronym}```", inline=True)
    embed.add_field(name=f"Market Rank:", value=f"```{rank}```", inline=True)
    embed.add_field(name=f"Price:", value=f"```{price}```", inline=True)
    embed.add_field(name=f"Market Cap:", value=f"```{market}```", inline=True)
    embed.add_field(name=f"Volume [24hrs]:", value=f"```{vol}```", inline=True)
    embed.add_field(name=f"Percent [24hrs]:", value=f"```{percent}```", inline=True)
    embed.add_field(name=f"Highest AllTime:", value=f"```{highest}```", inline=True)
    embed.add_field(name=f"Return YTD:", value=f"```{Rytd}```", inline=True)
    embed.add_field(name=f"Average Fee [24hrs]:", value=f"```{fee}```", inline=True)
    embed.set_footer(text=f"{name}'s info", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="rgame",
             description="Displays information about a Roblox game.",
             options=[
                 create_option(
                     name="url",
                     description="The URL of the Roblox game.",
                     option_type=3,
                     required=True
                 )
             ])
async def rgame(ctx: SlashContext, url: str):
    await ctx.defer()
    url1 = f"{url}"
    requestURL = requests.get(url1)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")
    player = soup.find('p', class_="text-lead font-caption-body wait-for-i18n-format-render").text
    visit = (soup.find('p', id='game-visit-count')['title'])
    fav = soup.find('span', class_="game-favorite-count").text
    name = soup.find('h1').text
    created = soup.find('p',class_="text-lead font-caption-body").text
    updated = soup.find_all('p', class_='text-lead font-caption-body')[1].text
    size = soup.find_all('p',class_="text-lead font-caption-body wait-for-i18n-format-render")[3].text
    embed=discord.Embed(title=f"Game info for {name} ", url=f"{url}", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
    embed.add_field(name=f"visits:", value=f"```{visit}```", inline=True)
    embed.add_field(name=f"favorites:", value=f"```{fav}```", inline=True)
    embed.add_field(name=f"player count:", value=f"```{player}```", inline=True)
    embed.add_field(name=f"Server Size:", value=f"```{size}```", inline=True)
    embed.add_field(name=f"Created:", value=f"```{created}```", inline=True)
    embed.add_field(name=f"Last Updated:", value=f"```{updated}```", inline=True)
    embed.set_footer(text=f"{name}'s Info", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@nsfw.error
async def nsfw(ctx,error):
    embed=discord.Embed(title="NSFW COMMAND ERROR", color=0xFF0400)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="THIS IS NOT AN NSFW CHANNEL", value=f"This command is NSFW and will need to be sent in NSFW channel", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064570023437422743/1195445329999867155jean_victor_balin_cross.svg.thumb.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@restart.error
async def restart(ctx,error):
    embed=discord.Embed(title="RESTART COMMAND ERROR", color=0xFF0400)
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Owner Only Command", value=f"You must be the owner of the server to use command.", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064570023437422743/1195445329999867155jean_victor_balin_cross.svg.thumb.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@bot.event
async def on_command_error(ctx, error:commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
            cmd = ctx.message.content.split()[0]
            cmd = cmd.lstrip(prefix)
            embed=discord.Embed(title="COMMAND ERROR", color=0xFF0400)
            embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
            embed.add_field(name="COMMAND NOT FOUND", value=f"The command {cmd} does not exist", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064570023437422743/1195445329999867155jean_victor_balin_cross.svg.thumb.png")
            embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
            embed.timestamp = datetime.datetime.utcnow()
            print(Fore.RED+f"[ERR] The Command {cmd} Does not exist"+Fore.RESET)
            await ctx.send(embed=embed, delete_after=30)
open_tickets = {}

@slash.slash(name="newticket", description="Create a new ticket.")
async def new_ticket(ctx: SlashContext):
    if ctx.channel.id != config['botcmds']:
        await ctx.send(f"This command can only be used in <#{config['botcmds']}>.", delete_after= 15)
        return
    if ctx.author.id in open_tickets:
        await ctx.send("You already have a ticket open.", delete_after=15)
        return
    category_name = "Tickets"
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    if not category:
        category = await ctx.guild.create_category(category_name)
    ticket_name = "Ticket-" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    ticket_channel = await ctx.guild.create_text_channel(ticket_name, category=category)
    await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    allowed_roles = [config['mod'], config['owner'], config['admin']]
    for role_id in allowed_roles:
        role = ctx.guild.get_role(role_id)
        if role is not None:
            await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)
    embed = discord.Embed(title="Ticket Created", description=f"Ticket created in {ticket_channel.mention}", color=discord.Color.green())
    await ctx.send(embed=embed)
    embed = discord.Embed(title="Welcome to Your Ticket", description=f"Thank you for contacting support, {ctx.author.mention}. We will assist you as soon as possible.", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ticket_channel.send(embed=embed)
    open_tickets[ctx.author.id] = ticket_channel

@slash.slash(name="closeticket", description="Close your ticket.")
async def close_ticket(ctx: SlashContext):
    if ctx.author.id not in open_tickets:
        await ctx.send("You don't have any tickets open.")
        return
    ticket_channel = open_tickets[ctx.author.id]
    await ctx.send("I hope we could help. Closing your ticket in 3 seconds...")
    for i in range(3, 0, -1):
        await asyncio.sleep(1)
        await ctx.message.edit(content=f"I hope we could help. Closing your ticket in {i} seconds...")
    await ticket_channel.delete()
    del open_tickets[ctx.author.id]


@slash.slash(name="ping", description="Check bot latency.")
async def ping(ctx: SlashContext):
    embed = discord.Embed(title="Pong!", description=f"Latency: {round(bot.latency * 1000)}ms", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="invite", description="Invite the bot to your server.")
async def invite(ctx: SlashContext):
    embed = discord.Embed(title="Invite Egglington", description="Click [here](https://discord.com/api/oauth2/authorize?client_id=1063758752160960573&permissions=8&scope=bot%20applications.commands) to invite the bot to your server.", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="support", description="Join the support server.")
async def support(ctx: SlashContext):
    embed = discord.Embed(title="Support Server", description="Click [here](https://discord.gg/https://discord.gg/AUevumCwXj) to join the support server.", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="vote", description="Vote for the bot.")
async def vote(ctx: SlashContext):
    embed = discord.Embed(title="Vote for Egglington", description="Click [here](https://top.gg/bot/1063758752160960573/vote) to vote for the bot.", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="github", description="View the bot's source code.")
async def github(ctx: SlashContext):
    embed = discord.Embed(title="Egglington's GitHub", description="Click [here](https://github.com/egg883/Egglington-Discord-bot) to view the bot's source code.", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="8ball", description="Ask the magic 8ball a question.")
async def eightball(ctx: SlashContext, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    embed = discord.Embed(title="8ball", description=f"Question: {question}\nAnswer: {random.choice(responses)}", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="coinflip", description="Flip a coin.")
async def coinflip(ctx: SlashContext):
    responses = [
        "Heads",
        "Tails"
    ]
    embed = discord.Embed(title="Coinflip", description=f"{random.choice(responses)}", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="rps", description="Play rock paper scissors.")
async def rps(ctx: SlashContext, *, choice):
    responses = [
        "Rock",
        "Paper",
        "Scissors"
    ]
    embed = discord.Embed(title="Rock Paper Scissors", description=f"Your choice: {choice}\nMy choice: {random.choice(responses)}", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="dice", description="Roll a dice.")
async def dice(ctx: SlashContext):
    responses = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
    ]
    embed = discord.Embed(title="Dice", description=f"{random.choice(responses)}", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="choose", description="Choose between multiple options.")
async def choose(ctx: SlashContext, *, options):
    embed = discord.Embed(title="Choose", description=f"{random.choice(options.split())}", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="poll", description="Create a poll.")
async def poll(ctx: SlashContext, *, question):
    embed = discord.Embed(title="Poll", description=f"{question}", color=discord.Color.blue())
    embed.set_author(name="Egglington", url="https://egg883.xyz", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.xyz", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.timestamp = datetime.datetime.utcnow()
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

#////////////////////////////////////////////////////////////////////////// 
def Init():
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    config.get('bottoken')
    try:
        bot.run(bottoken)
    except discord.errors.LoginFailure:
        input(f"{Fore.RED}[SYSTEM] BOT TOKEN IS INVALID CHECK CONFIG"+Colours.White)
        sys.exit
        python = sys.executable
        os.execl(python, python, * sys.argv)
Init()
