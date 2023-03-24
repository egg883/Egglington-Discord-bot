import aiohttp
import datetime
import time
import io
import json
import os
import openai
import discord
from colorama import Fore
import random
import string
import ctypes
import re
import sys
from discord_interactions import *
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_select, create_select_option
from discord_components import DiscordComponents
from roblox import Client
import asyncio
import requests
from bs4 import BeautifulSoup
import random
from discord_components import Button, Select, SelectOption, ComponentsBot, interaction
from discord_components.component import ButtonStyle
import urllib
from discord.utils import find
import urllib.request
from typing import Dict
import time
#//////////////////////////////////////////////////////////////////////////
client1 = Client()
class Colours:
    White = "\x1b[38;2;250;250;250m"
    Magenta = "\x1b[38;2;255;94;255m"
os.system("color")
config = json.load(open('config.json', 'rb'))
clientsec = config['clientsecret']
clientid = config['clientid']
bottoken = config['bot_token']
prefix = config['prefix']
deletein = config['deletetime']
ownerrole = config['owner']
adminrole = config['admin']
modrole = config['mod']
botcmds = config['botcmds']
server = config['serverid']
logs = config['logs']
playingstatus = config['status']
playingstatus2 = config['status2']
welc = config['welcome']
embed_color = 0xfcd005
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = prefix, intents=intents, help_command=None)
cmds = {len(bot.commands)}
version = "1.1.1"
slash = SlashCommand(bot, sync_commands=True)
DiscordComponents(bot)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.members = True
openai.api_key = "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"
githuburl = "https://github.com/egg883/Egglington-Discord-bot"
def restart_bot(): 
  os.execv(sys.executable,sys.argv)
#//////////////////////////////////////////////////////////////////////////
def new_splash():
    print(f'{Colours.Magenta}Egglington is now Listening to {len(bot.guilds)} servers')
    print(f"{Colours.Magenta}Egglington's Prefix is {prefix}")
    print(f"{Colours.Magenta}Do {prefix}help for the help commands")

CHANNEL_ID = config['logs']
allowed_guild_ids = [config['serverid']]

@bot.event
async def on_member_ban(guild, user):
    if guild.id not in allowed_guild_ids:
        return
    
    embed = discord.Embed(title="User Banned", color=discord.Color.red())
    embed.add_field(name="User", value="{0} ({1})".format(user.name, user.id))
    embed.add_field(name="Guild", value="{0.name} ({0.id})".format(guild))
    embed.add_field(name="Reason", value="No reason provided", inline=False)
    audit_logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
    if audit_logs:
        audit_log = audit_logs[0]
        if audit_log.target == user:
            if audit_log.reason:
                embed.set_field_at(2, name="Reason", value=audit_log.reason, inline=False)
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    if member.guild.id not in allowed_guild_ids:
        return
    
    embed = discord.Embed(title="User Kicked", color=discord.Color.dark_gold())
    embed.add_field(name="User", value="{0.name} ({0.id})".format(member))
    embed.add_field(name="Guild", value="{0.name} ({0.id})".format(member.guild))
    embed.add_field(name="Reason", value="No reason provided", inline=False)
    audit_logs = await member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
    if audit_logs:
        audit_log = audit_logs[0]
        if audit_log.target == member:
            if audit_log.reason:
                embed.set_field_at(2, name="Reason", value=audit_log.reason, inline=False)
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if message.guild.id not in allowed_guild_ids:
        return
    
    embed = discord.Embed(title="Message Deleted", color=discord.Color.dark_blue())
    embed.add_field(name="Channel", value="{0.channel.name} ({0.channel.id})".format(message))
    embed.add_field(name="Guild", value="{0.guild.name} ({0.guild.id})".format(message))
    if message.content:
        embed.add_field(name="Content", value=message.content)
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)


@bot.event
async def on_guild_channel_delete(channel):
    if channel.guild.id not in allowed_guild_ids:
        return
    
    embed = discord.Embed(title="Channel Deleted", color=discord.Color.dark_orange())
    embed.add_field(name="Channel", value="{0.name} ({0.id})".format(channel))
    embed.add_field(name="Guild", value="{0.guild.name} ({0.guild.id})".format(channel))
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)

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
    title = ctypes.windll.kernel32.SetConsoleTitleW(f"Egglington Client | Version: [v{version}]  | Commands: [{len(bot.commands)}]") 
    time.sleep(1)
    title
    new_splash()

def Clear():
    os.system('cls')
#//////////////////////////////////////////////////////////////////////////
async def ch_pr():
 await bot.wait_until_ready()
 statuses = [f"{playingstatus} || {playingstatus2}", f"listening on {len(bot.guilds)} servers", f"Still need help? do {prefix}help for more help!"]
 while not bot.is_closed():
   status = random.choice(statuses)
   await bot.change_presence(activity=discord.Game(name=status))
   await asyncio.sleep(10)
bot.loop.create_task(ch_pr())

@bot.command()
async def clearconsole(ctx):
    ctx.message.delete()
    Clear()
    new_splash()

@bot.command()
async def help(ctx):
    guild = ctx.guild
    embed=discord.Embed(title="Help commands", url="https://egg883.shop", description="This is help section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] general", value="List of general commands", inline=False)
    embed.add_field(name=f"[{prefix}] moderation", value="List of moderation commands", inline=False)
    embed.add_field(name=f"[{prefix}] server", value="List of server commands", inline=False)
    embed.add_field(name=f"[{prefix}] nsfw", value="List of nsfw commands", inline=False)
    embed.add_field(name=f"[{prefix}] memes", value="List of memes commands", inline=False)
    embed.add_field(name=f"[{prefix}] fun", value="List of fun commands", inline=False)
    embed.add_field(name=f"[{prefix}] crypto", value="List of crypto commands", inline=False)
    embed.add_field(name=f"[{prefix}] roblox", value="List of roblox commands", inline=False)
    embed.add_field(name=f"[{prefix}] settings", value="List of settings commands", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@bot.command()
async def memes(ctx):
    embed=discord.Embed(title="Meme Commands", url="https://egg883.shop", description="This is Meme section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] ph", value=f"[{prefix}] ph (@user) (text)", inline=False)
    embed.add_field(name=f"[{prefix}] jail", value=f"[{prefix}] jail (@user)", inline=False)
    embed.add_field(name=f"[{prefix}] wasted", value=f"[{prefix}] wasted (@user)", inline=False)
    embed.add_field(name=f"[{prefix}] horny", value=f"[{prefix}] horny (@user)", inline=False)
    embed.add_field(name=f"[{prefix}] lolice", value=f"[{prefix}] lolice (@user)", inline=False)
    embed.add_field(name=f"[{prefix}] pixel", value=f"[{prefix}] pixel (@user)", inline=False)
    embed.add_field(name=f"[{prefix}] clyde", value=f"[{prefix}] clyde (text)", inline=False)
    embed.add_field(name=f"[{prefix}] trump", value=f"[{prefix}] trump (text)", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def general(ctx):
    embed=discord.Embed(title="General commands", url="https://egg883.shop", description="This is general section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] whois", value=f"[{prefix}] whois (@user)", inline=False)
    embed.add_field(name=f"[{prefix}] yt", value=f"[{prefix}] yt (name of yt video)", inline=False)
    embed.add_field(name=f"[{prefix}] vote", value=f"Vote for egglington", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def fun(ctx):
    embed=discord.Embed(title="Fun commands", url="https://egg883.shop", description="This is fun section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] pp", value=f"[{prefix}] pp (@user)", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def server(ctx):
    embed=discord.Embed(title="Server commands", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] role", value=f"[{prefix}] role (@user rolename)", inline=False)
    embed.add_field(name=f"[{prefix}] deleterole", value=f"[{prefix}] deleterole (rolename)", inline=False)
    embed.add_field(name=f"[{prefix}] first", value=f"[{prefix}] first", inline=False)
    embed.add_field(name=f"[{prefix}] spfp", value=f"[{prefix}] spfp", inline=False)
    embed.add_field(name=f"[/] newticket", value=f"Creates a ticket for help (Must be in botcmds)", inline=False)
    embed.add_field(name=f"[/] closeticket", value=f"Closes ticket", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def crypto(ctx):
    embed=discord.Embed(title="Crypto commands", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] btc", value=f"Displays current btc price", inline=False)
    embed.add_field(name=f"[{prefix}] sol", value=f"Displays current sol price", inline=False)
    embed.add_field(name=f"[{prefix}] eth", value=f"Displays current eth price", inline=False)
    embed.add_field(name=f"[{prefix}] usdt", value=f"Displays current usdt price", inline=False)
    embed.add_field(name=f"[{prefix}] ltc", value=f"Displays current ltc price", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def moderation(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="moderation commands", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] mute", value=f"[{prefix}] mute (reason) | [{prefix}] unmute (reason)", inline=False)
    embed.add_field(name=f"[{prefix}] purge", value=f"[{prefix}] purge (amount)", inline=False)
    embed.add_field(name=f"[{prefix}] ban", value=f"[{prefix}] ban (@user, reason) | {prefix} unban (@user, reason)", inline=False)
    embed.add_field(name=f"[{prefix}] kick", value=f"[{prefix}] kick (@user, reason)", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def roblox(ctx):
    embed=discord.Embed(title="Roblox Commands", url="https://egg883.shop", description="This is roblox section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
    embed.add_field(name=f"[{prefix}] ruser", value=f"[{prefix}] ruser (robloxusername)", inline=False)
    embed.add_field(name=f"[{prefix}] routfit", value=f"[{prefix}] routfit (robloxusername)", inline=False)
    embed.add_field(name=f"[{prefix}] ruserhis", value=f"[{prefix}] ruserhis (robloxusername)", inline=False)
    embed.add_field(name=f"[{prefix}] rvalue", value=f"[{prefix}] rvalue (robloxusername)", inline=False)
    # embed.add_field(name=f"[{prefix}] ritem", value=f"[{prefix}] ritem (item url)", inline=False)
    embed.add_field(name=f"[{prefix}] rgame", value=f"[{prefix}] rgame (game url)", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def settings(ctx):
    embed=discord.Embed(title="moderation commands", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] info", value=f"[{prefix}] info", inline=False)
    embed.add_field(name=f"[{prefix}] news", value=f"[{prefix}] news", inline=False)
    embed.add_field(name=f"[{prefix}] support", value=f"[{prefix}] support (dms only)", inline=False)
    embed.add_field(name=f"[{prefix}] restart", value=f"[{prefix}] restart (owner role only)", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed,delete_after=deletein)


@bot.command(pass_context=True)
@commands.has_any_role(ownerrole, modrole, adminrole) 
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    embed=discord.Embed(title="Purge command", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Purged", value=f"I have purged {limit} Messages")
    await ctx.send(embed=embed,delete_after=config['deletetime'])

@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.has_any_role(ownerrole, modrole, adminrole) 
async def mute(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed,delete_after=config['deletetime'])
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

@bot.command()
@commands.has_any_role(ownerrole, modrole, adminrole)
async def unmute(ctx,member: discord.Member, *, reason=None):
        await ctx.message.delete()
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted ", colour=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed,delete_after=config['deletetime'])
        await member.remove_roles(mutedRole, reason=reason)
        await member.send(f" You have been unmuted in: {guild.name} reason: {reason}")

@bot.command()
async def whois(ctx,*,member: discord.Member):
        await ctx.message.delete()
        embed = discord.Embed(title=f"Info about **{member.display_name}**", colour=0x007bff)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"Egglington", url="https://egg883.shop", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name="User ID:", value=f"```{member.id}```", inline=False)
        embed.add_field(name="Users Discriminator:", value=f"```#{member.discriminator}```", inline=True)
        embed.add_field(name="Creation Date:", value=f"```{member.created_at.strftime('%d/%m/%Y')}```", inline=True)
        embed.add_field(name="Server Join Date:", value=f"```{member.joined_at.strftime('%d/%m/%Y')}```", inline=True)
        embed.add_field(name="Is a bot:", value=f"```{member.bot}```", inline=True)
        await ctx.send(embed=embed,delete_after=60)

@bot.command()
@commands.has_any_role(ownerrole, modrole, adminrole) 
@commands.has_permissions(manage_messages=True)
async def role(ctx,member: discord.Member,*, rname):
    await ctx.message.delete()
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name=f"{rname}")
    if not mutedRole:
        mutedRole = await guild.create_role(name=f"{rname}")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=True, send_messages=True, read_message_history=True, read_messages=True)
        embed = discord.Embed(title="Created Role", colour=0x007bff)
        embed.set_author(name=f"Egglington", url="https://egg883.shop", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name="Created role:", value=f"The Role: {rname} Has successfully been given to {member.display_name}", inline=False)
        await member.add_roles(mutedRole)
        await ctx.send(embed=embed, delete_after=60)

@bot.command()
@commands.has_any_role(ownerrole, modrole, adminrole) 
async def deleterole(ctx, *, role: discord.Role = None):
    await ctx.message.delete()
    if ctx.author.guild_permissions.administrator and role:
        guild = ctx.guild
        if role in guild.roles:
            await role.delete()
            return
        embed = discord.Embed(title=F"Deleted Role", colour=0x007bff)
        embed.set_author(name=f"Egglington", url="https://egg883.shop", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name=f"{ctx.author.display_name} ", value=f"The Role: {role} Has been Deleted", inline=False)
        await ctx.send(embed=embed, delete_after=60)

@bot.command()
async def pp(ctx, *, user: discord.Member = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    size = random.randint(1, 15)
    dong = ""
    for _i in range(0, size):
        dong += "="
    embed = discord.Embed(title=F"PP command executed!", url="https://egg883.shop", colour=0x007bff)
    embed.set_author(name=f"Egglington", url="https://egg883.shop", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name=f"{user}'s PP size is: ", value=f"8{dong}D", inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@bot.command()
@commands.has_any_role(ownerrole, adminrole) 
async def unban(ctx, member:discord.User, *, reason=None):
    await ctx.message.delete()
    if reason == None:
        reason = f"No Reason Provided"
    await ctx.guild.unban(member, reason=reason)
    embed11 = discord.Embed(title="Unbanned!", description=f"{member.mention} Has been Ressurected", colour=0x007bff)
    embed11.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed11.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063813203445944420/94-940113_file-ban-hammer-png-roblox-ban-hammer-png_1.png")
    embed11.add_field(name="reason:", value=reason, inline=False)
    embed = discord.Embed(title="Unban Log", description=f"{member.mention} has been **unbanned** by {ctx.author.mention}\n\nReason: `{reason}`\n\nUnbanned from: `{ctx.guild.name}`", color=0x1355ed)
    embed.add_field(name="User", value=f"{member}", inline=True)
    embed.add_field(name="UserID", value=f"{member.id}", inline=True)
    embed.add_field(name="Moderator", value=f"{ctx.author}", inline=True)
    embed.set_footer(text=f"Unban log - Banned user: {member.name}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed11, delete_after=15)
    logchannel = config['logs']
    await logchannel.send(embed=embed)
    await ctx.message.delete()
    print("Command Executed")

@bot.command()
@commands.has_any_role(ownerrole, adminrole) 
async def ban(ctx, member:discord.User, *, reason=None):
    await ctx.message.delete()
    if reason == None:
        reason = f"No Reason Provided"
    guild = ctx.guild
    await member.send(f" You have been Banished from: {guild.name} reason: {reason}")
    await member.ban(reason=reason)
    embed11 = discord.Embed(title="Banned!", description=f"{member.mention} Has been hit with the hammer ", colour=0x007bff)
    embed11.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed11.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063813203445944420/94-940113_file-ban-hammer-png-roblox-ban-hammer-png_1.png")
    embed11.add_field(name="reason:", value=reason, inline=False)
    embed = discord.Embed(title="Ban Log", description=f"{member.mention} has been **Banned** by {ctx.author.mention}\n\nReason: `{reason}`\n\nBanned from: `{ctx.guild.name}`", color=0x1355ed)
    embed.add_field(name="User", value=f"{member}", inline=True)
    embed.add_field(name="UserID", value=f"{member.id}", inline=True)
    embed.add_field(name="Moderator", value=f"{ctx.author}", inline=True)
    embed.set_footer(text=f"ban log - Banned user: {member.name}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed11, delete_after=15)
    logchannel = config['logs']
    await logchannel.send(embed=embed)
    await ctx.message.delete()
    print("Command Executed")

@bot.command()
@commands.has_any_role(ownerrole, modrole, adminrole) 
async def kick(ctx, member:discord.User, *, reason=None):
    await ctx.message.delete()
    guild = ctx.guild
    await member.send(f" You have been kicked from: {guild.name} reason: {reason}")
    await member.kick()
    if reason == None:
        reason = "No Reason Specified"
    embed11 = discord.Embed(title="kicked!", description=f"{member.mention} Has been booted out of the server", colour=0x007bff)
    embed11.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed11.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063823799490986054/8495-moderation-icon.png")
    embed11.add_field(name="reason:", value=reason, inline=False)
    embed = discord.Embed(title="Kick Log", description=f"{member.mention} has been **Kicked** by {ctx.author.mention}\n\nReason: `{reason}`\nKicked from: `{ctx.guild.name}`", color=0x1355ed)
    embed.add_field(name="User", value=f"{member}", inline=True)
    embed.add_field(name="UserID", value=f"{member.id}", inline=True)
    embed.add_field(name="Moderator", value=f"{ctx.author}", inline=True)
    embed.set_footer(text=f"Kick log - Kicked user: {member.name}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed11, delete_after=15)
    logchannel = config['logs']
    await logchannel.send(embed=embed)

@bot.command()
@commands.has_any_role(ownerrole) 
async def restart(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="Command Executed", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1072208453323460790/giphy.gif")
    embed.add_field(name="**Please Wait**", value="Bot Is Restarting.", inline=False)
    await ctx.send(embed=embed, delete_after=600)
    print("restarting bot")
    restart_bot()


@bot.command()
async def news(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title=f"Update V{version}", description=f"This is the latest news about our bot Update", url=f"{githuburl}", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Added Crypto catagory", value="```added crypto prices```", inline=False)
    embed.add_field(name="stupid gay ritem broke", value="```Removed ritem due to issues```", inline=False)
    embed.add_field(name="Our Website", value="```https://egg883.shop```", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def vote(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title=f"Vote for Egglington", url=f"https://top.gg/bot/1063758752160960573", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Vote for us", value="https://top.gg/bot/1063758752160960573", inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    await ctx.send(embed=embed)

@commands.dm_only()
@bot.command()
async def support(ctx):
    embed = discord.Embed(title="Support Panel", description=f"This is the support panel of our bot", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Need help? Join our discord: ", value="https://discord.gg/AUevumCwXj", inline=False)
    embed.add_field(name="Or contact our email", value="egg@egg883.shop", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def sinfo(ctx):
    await ctx.message.delete()
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    guild = ctx.guild
    categories = len(ctx.guild.categories)
    member_count = len(ctx.guild.members)
    channels = text_channels + voice_channels
    embed = discord.Embed(title="Server Info", description=f"This is info about **{guild.name}**", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url=f"{guild.icon_url}")
    embed.add_field(name="Server ID", value=f"```{ctx.guild.id}```", inline=False)
    embed.add_field(name="Channel Count", value=f"```{channels} Channels {text_channels} Text, {voice_channels} Voice, {categories}```", inline=False)
    embed.add_field(name="Server Owner", value=f"```{ctx.guild.owner}```", inline=True)
    embed.add_field(name="Member Count", value=f"```{member_count}```", inline=True)
    embed.add_field(name="Server Verification", value=f"```{str(ctx.guild.verification_level).upper()}```", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Info", description=f"This is a information page about my bot", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Total Commands:", value = f"```{len(bot.commands)}```", inline=True)
    embed.add_field(name="Prefix:", value=f"```{prefix}```", inline=True)
    embed.add_field(name="Version:", value=f"```{version}```", inline=True)
    embed.add_field(name="Creator:", value="```This bot was made by eggs#6666 this is a little project i wanted todo```", inline=False)
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@bot.command()
async def first(ctx):
    await ctx.message.delete()
    channel = ctx.channel
    first_message = (await channel.history(limit = 1, oldest_first = True).flatten())[0]
    embed = discord.Embed(title="First message", description=f"This is the first ever message sent in this channel", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="First Message Content", value = f"{first_message.content}", inline=False)
    embed.add_field(name="First Message link", value = f"{first_message.jump_url}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def spfp(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}'s Server Icon", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_image(url=f"{guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    await ctx.send(embed=embed, delete_after=deletein)

@bot.command()
async def jail(ctx, member=None):
    await ctx.message.delete()
    if member==None:
        member = ctx.message.author
    else:
        member = ctx.message.mentions[0]
        member = await bot.fetch_user(int(member.id))
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read()) 
            
            await trigSession.close()
            
            await ctx.send(file=discord.File(imageData, 'eggui.gif'))


@bot.command()
async def ruser(ctx, user423):
    user = await client1.get_user_by_username(user423)
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
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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
        embed.set_footer(text=f"{user423}'s Information", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@bot.command()
async def routfit(ctx, user423):
    user = await client1.get_user_by_username(user423)
    user_thumbnails = await client1.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        size=(420, 420)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        embed=discord.Embed(title=f"Found current outfit for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name=f"Username:", value=f"{user.name}", inline=False)
        embed.set_image(url = f"{user_thumbnail.image_url}")
        embed.set_footer(text=f"{user423}'s current outfit", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@bot.command()
async def wasted(ctx, member=None):
    await ctx.message.delete()
    if member==None:
        member = ctx.message.author
    else:
        member = ctx.message.mentions[0]
        member = await bot.fetch_user(int(member.id))
        
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read()) 
            
            await trigSession.close()
            
            await ctx.send(file=discord.File(imageData, 'eggui.gif'))

@bot.command(aliases=['youtube','yt'])
async def _youtube(ctx, *, search):
    await ctx.message.delete()
    author=ctx.message.author
    guild=ctx.guild
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_content= html_content.read().decode()
    search_results = re.findall(r'\/watch\?v=\w+', search_content)
    await ctx.send(f'{author.mention} result for {search}:\n https://www.youtube.com' + search_results[0])

@bot.command()
async def lolice(ctx, member=None):
    await ctx.message.delete()
    if member==None:
        member = ctx.message.author
    else:
        member = ctx.message.mentions[0]
        member = await bot.fetch_user(int(member.id))
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/lolice?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read()) 
            
            await trigSession.close()
            
            await ctx.send(file=discord.File(imageData, 'eggui.gif'))

@bot.command()
async def trump(ctx, *, msg):
    await ctx.message.delete()
    response = requests.get(f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={msg}")
    stuff = json.loads(response.text)
    embed=discord.Embed(title="Meanwhile on twitter:", color=0x007bff, timestamp=ctx.message.created_at)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_image(url = stuff['message'])
    await ctx.send(embed=embed, delete_after = deletein)

@bot.command()
async def ph(ctx, member=None, *, msg):
    if member==None:
        member = ctx.message.author
    else:
        member = ctx.message.mentions[0]
        member = await bot.fetch_user(int(member.id))
    await ctx.message.delete()
    url = member.avatar_url_as(format="png")
    response = requests.get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={url}&username={member.display_name}&text={msg}")
    stuff = json.loads(response.text)
    embed=discord.Embed(title="Pornhub Comment Section:", color=0x007bff, timestamp=ctx.message.created_at)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_image(url = stuff['message'])
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after = deletein)


@bot.command()
async def horny(ctx, member=None):
    await ctx.message.delete()
    if member==None:
        member = ctx.message.author
    else:
        member = ctx.message.mentions[0]
        member = await bot.fetch_user(int(member.id))
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read()) 
            
            await trigSession.close()
            
            await ctx.send(file=discord.File(imageData, 'eggui.gif'))

@bot.command()
async def clyde(ctx,*, msg):
    await ctx.message.delete()
    response = requests.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={msg}")
    stuff = json.loads(response.text)
    embed=discord.Embed(title="Clyde has a message for you", color=0x007bff, timestamp=ctx.message.created_at)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_image(url = stuff['message'])
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after = deletein)

@bot.command()
async def pixel(ctx, member=None):
    await ctx.message.delete()
    if member==None:
        member = ctx.message.author
    else:
        member = ctx.message.mentions[0]
        member = await bot.fetch_user(int(member.id))
    async with aiohttp.ClientSession() as trigSession:
        async with trigSession.get(f'https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
            imageData = io.BytesIO(await trigImg.read()) 
            
            await trigSession.close()
            
            await ctx.send(file=discord.File(imageData, 'eggui.gif'))

@commands.is_nsfw()
@bot.command()
async def nsfw(ctx, category=None):
    await ctx.message.delete()
    if category is None:
        embed=discord.Embed(title="NSFW Commands", description = "**THESE MUST BE SENT IN AN NSFW CHANNEL**", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name="NSFW Command Usage", value = f"[{prefix}] nsfw (catagory name)", inline=False)
        embed.add_field(name="**NSFW Catagories**", value=f"tentacle\nhass\nhmidriff\npgif\n4k\nholo\nhboobs\npussy\nhthigh\nthigh", inline=True)
        await ctx.send(embed=embed, delete_after=deletein)
 
    elif str(category).lower() == "tentacle":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=tentacle')
        res = r.json()
        embed=discord.Embed(title="Tentacle", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "hass":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=hass')
        res = r.json()
        embed=discord.Embed(title="Hentai Ass", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "hmidriff":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=hmidriff')
        res = r.json()
        embed=discord.Embed(title="hmidriff", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "pgif":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=pgif')
        res = r.json()
        embed=discord.Embed(title="pgif", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)
        
    elif str(category).lower() == "4k":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=4k')
        res = r.json()
        embed=discord.Embed(title="4k", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "hentai":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=hentai')
        res = r.json()
        embed=discord.Embed(title="hentai", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "holo":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=holo')
        res = r.json()
        embed=discord.Embed(title="holo", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "hboobs":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=hboobs')
        res = r.json()
        embed=discord.Embed(title="hboobs", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "pussy":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=pussy')
        res = r.json()
        embed=discord.Embed(title="pussy", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "hthigh":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=hthigh')
        res = r.json()
        embed=discord.Embed(title="hthigh", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

    elif str(category).lower() == "thigh":    
        r = requests.get(f'https://nekobot.xyz/api/image?type=thigh')
        res = r.json()
        embed=discord.Embed(title="thigh", color=0x007bff, timestamp=ctx.message.created_at)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
 
        embed.set_image(url=res['message'])
        await ctx.send(embed=embed, delete_after=deletein)

@bot.command() # THANKS TO PAW
async def ruserhis(ctx,user423):
    user = await client1.get_user_by_username(user423)
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
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_thumbnail(url=f"{user_thumbnail.image_url}")
        embed.add_field(name=f"Past usernames", value=f"```{users}```", inline=False)
        embed.set_footer(text=f"{user423}'s Past Usernames", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@bot.command() 
async def rvalue(ctx,username):
    user = await client1.get_user_by_username(username)
    userid = user.id
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
    soup = BeautifulSoup(content, "html.parser")
    URL3 = f"https://www.rolimons.com/player/{userid}"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup1 = BeautifulSoup(content, "html.parser")
    URL3 = f"https://rblx.trade/u/{username}"
    requestURL = requests.get(URL3)
    content = requestURL.content
    soup = BeautifulSoup(content, "html.parser")  
    test_json = json.loads(soup.find('script', id="__NEXT_DATA__").string)
    collect = format(max([x['roblox_itemcount'] for x in test_json['props']['pageProps']['inventoryHistory'] if x['roblox_itemcount'] < 15000]), ",")
    trade = soup1.find('span',class_="card-title mb-1 text-light stat-data text-nowrap").text
    embed=discord.Embed(title=f"Rolimons Info for {user.name} ", url=f"https://www.rolimons.com/player/{userid}", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url=f"{user_thumbnail.image_url}")
    embed.add_field(name=f"Username:", value=f"```{listofusers1['name']}```", inline=True)
    embed.add_field(name=f"Rank:", value=f"```{listofusers1['rank']}```", inline=True)
    embed.add_field(name=f"RAP:", value=f"```{listofusers1['rap']}```", inline=True)
    embed.add_field(name=f"Value:", value=f"```{listofusers1['value']}```", inline=True)
    embed.add_field(name=f"Collectibles:", value=f"```{collect}```", inline=True)
    embed.add_field(name=f"Trade ads:", value=f"```{trade}```", inline=True)
    embed.add_field(name=f"Premium:", value=f"```{listofusers1['premium']}```", inline=True)
    embed.add_field(name=f"Terminated:", value=f"```{listofusers1['terminated']}```", inline=True)
    embed.add_field(name=f"Private:", value=f"```{listofusers1['privacy_enabled']}```", inline=True)
    embed.add_field(name=f"Last Location:", value=f"```{listofusers1['last_location']}```", inline=True)
    embed.set_footer(text=f"{username}'s rolimons", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1079482029776842812/JCiYruAM_400x400.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@bot.command(aliases=['btc','bitcoin', '#1'])
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
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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

@bot.command(aliases=['eth','ethereum', '#2'])
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
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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

@bot.command(aliases=['sol','solana', '#11'])
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
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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

@bot.command(aliases=['tether','usdt', '#3'])
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
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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

@bot.command(aliases=['litecoin','ltc', '#15'])
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
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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

@bot.command()
async def rgame(ctx, url):
    await ctx.message.delete()
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
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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

@support.error
async def support(ctx,error):
    embed=discord.Embed(title="SUPPORT COMMAND ERROR", color=0xFF0400)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="This command is only enabled for dms", value=f"DM the bot to preview this command!", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064570023437422743/1195445329999867155jean_victor_balin_cross.svg.thumb.png")
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@nsfw.error
async def nsfw(ctx,error):
    embed=discord.Embed(title="NSFW COMMAND ERROR", color=0xFF0400)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="THIS IS NOT AN NSFW CHANNEL", value=f"This command is NSFW and will need to be sent in NSFW channel", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064570023437422743/1195445329999867155jean_victor_balin_cross.svg.thumb.png")
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@restart.error
async def restart(ctx,error):
    embed=discord.Embed(title="RESTART COMMAND ERROR", color=0xFF0400)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Owner Only Command", value=f"You must be the owner of the server to use command.", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064570023437422743/1195445329999867155jean_victor_balin_cross.svg.thumb.png")
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@bot.event
async def on_command_error(ctx, error:commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
            cmd = ctx.message.content.split()[0]
            cmd = cmd.lstrip(prefix)
            embed=discord.Embed(title="COMMAND ERROR", color=0xFF0400)
            embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
            embed.add_field(name="COMMAND NOT FOUND", value=f"The command {cmd} does not exist", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1064570023437422743/1195445329999867155jean_victor_balin_cross.svg.thumb.png")
            embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_footer(text="https://egg883.shop", icon_url = "https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
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
