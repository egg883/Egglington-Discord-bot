from asyncio.windows_events import NULL
import asyncio
import aiohttp
import re
from win10toast import ToastNotifier
from requests.utils import CaseInsensitiveDict
from itertools import cycle
from colour import Color
import datetime
import time
import datetime, io, random
from colorama import Fore, init
import sys
import json
import urllib
import os
import discord
from discord import embeds, guild, message, user
import ctypes
from pypresence import Presence, presence
from discord.embeds import Embed
import requests, wmi
from discord.ext.commands import MissingPermissions
import psutil
from gtts import gTTS
import tasks
from discord.ext.commands import Bot, guild_only
from discord.ext import commands
from roblox import Client
import discord_slash
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
owner = config['owner']
admin = config['admin']
botowner = config['botowner']
mod = config['mod']
bot = commands.Bot(command_prefix= prefix)
cmds = {len(bot.commands)}
intents = discord.Intents.all()
version = 1.2
intents.members = True
slash = discord_slash.SlashCommand(bot, sync_commands=True)  
#//////////////////////////////////////////////////////////////////////////
def new_splash():
    print(f'{Colours.Magenta}Egglington is now Listening to {len(bot.guilds)} servers')

@bot.event
async def on_connect():
    title = ctypes.windll.kernel32.SetConsoleTitleW(f"Egglington Client | Version: [{version}]  | Commands: [{len(bot.commands)}]") 
    time.sleep(1)
    title
    new_splash()

def Clear():
    os.system('cls')

#//////////////////////////////////////////////////////////////////////////
async def ch_pr():
 await bot.wait_until_ready()
 statuses = [f"Scrambled Egg, boiled Egg or Regular? || {prefix}h for help",f"listening on {len(bot.guilds)} server's",f"Still need help? do {prefix}h for more help!"]
 while not bot.is_closed():
   status = random.choice(statuses)
   await bot.change_presence(activity=discord.Game(name=status))
   await asyncio.sleep(10)
bot.loop.create_task(ch_pr())

@bot.event
async def on_message(message):
	if message.content == "cheese":
		await message.channel.send("Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
	await bot.process_commands(message)

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong",delete_after=config['deletetime'])


@bot.command()
async def ruser(ctx, user423):
    await ctx.message.delete()
    user = await client1.get_user_by_username(user423)
    user_thumbnails = await client1.thumbnails.get_user_avatar_thumbnails(
        users=[user],
        size=(420, 420)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        embed=discord.Embed(title=f"Found Info for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x007bff)
        embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.set_thumbnail(url=f"{user_thumbnail.image_url}")
        embed.add_field(name=f"Username:", value=f"{user.name}", inline=False)
        embed.add_field(name=f"Display name:", value=f"{user.display_name}", inline=False)
        embed.add_field(name=f"User ID:", value=f"{user.id}", inline=False)
        embed.add_field(name=f"Creation Date:", value=f"{user.created.strftime('%d/%m/%Y')}", inline=False)
        embed.add_field(name=f"Is banned:", value=f"{user.is_banned}", inline=False)
        embed.add_field(name=f"Description:", value=f"{user.description}", inline=False)
        embed.set_footer(text=f"{user423}'s Information", icon_url= "https://cdn.discordapp.com/attachments/1063774865729007616/1064493888921948200/gamer-logo-roblox-6_1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed,delete_after=60)



@bot.slash_command(name = "help", description = "This is the help panel")
@bot.command()
async def h(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    embed=discord.Embed(title="Help commands", url="https://egg883.shop", description="This is help section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] general", value="List of general commands", inline=False)
    embed.add_field(name=f"[{prefix}] moderation", value="List of moderation commands", inline=False)
    embed.add_field(name=f"[{prefix}] server", value="List of server commands", inline=False)
    embed.add_field(name=f"[{prefix}] memes", value="List of memes commands", inline=False)
    embed.add_field(name=f"[{prefix}] fun", value="List of fun commands", inline=False)
    embed.add_field(name=f"[{prefix}] roblox", value="List of roblox commands", inline=False)
    embed.add_field(name=f"[{prefix}] settings", value="List of settings commands", inline=False)
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def general(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="General commands", url="https://egg883.shop", description="This is general section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] whois", value=f"[{prefix}] whois (@user)", inline=False)
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def server(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="Server commands", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] role", value=f"[{prefix}] role (@user rolename)", inline=False)
    embed.add_field(name=f"[{prefix}] deleterole", value=f"[{prefix}] deleterole (rolename)", inline=False)
    embed.add_field(name=f"[{prefix}] first", value=f"[{prefix}] first", inline=False)
    embed.add_field(name=f"[{prefix}] spfp", value=f"[{prefix}] spfp", inline=False)
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
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def roblox(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="Roblox Commands", url="https://egg883.shop", description="This is roblox section of the bot", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] ruser", value=f"[{prefix}] ruser (robloxusername)", inline=False)
    await ctx.send(embed=embed,delete_after=deletein)

@bot.command()
async def settings(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="moderation commands", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name=f"[{prefix}] info", value=f"[{prefix}] info", inline=False)
    embed.add_field(name=f"[{prefix}] news", value=f"[{prefix}] news", inline=False)
    await ctx.send(embed=embed,delete_after=deletein)


@bot.command(pass_context=True)
@commands.has_any_role(owner, mod, admin, botowner) 
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    embed=discord.Embed(title="Purge command", url="https://egg883.shop", color=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.add_field(name="Purged", value=f"I have purged {limit} Messages")
    await ctx.send(embed=embed,delete_after=config['deletetime'])

@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.has_any_role(owner, mod, admin, botowner) 
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
@commands.has_any_role(owner, mod, admin, botowner)
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
        embed = discord.Embed(title=f"Info about {member.display_name}", colour=0x007bff)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"Egglington", url="https://egg883.shop", icon_url=f"https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
        embed.add_field(name="User ID:", value=f"{member.id}", inline=False)
        embed.add_field(name="Users Discriminator:", value=f"{member.discriminator}", inline=False)
        embed.add_field(name="Creation Date:", value=f"{member.created_at.strftime('%d/%m/%Y')}", inline=False)
        embed.add_field(name="Server Join Date:", value=f"{member.joined_at.strftime('%d/%m/%Y')}", inline=False)
        embed.add_field(name="Is a bot:", value=f"{member.bot}", inline=False)
        await ctx.send(embed=embed,delete_after=60)

@bot.command()
@commands.has_any_role(owner, mod, admin, botowner) 
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
@commands.has_any_role(owner, mod, admin, botowner) 
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
async def clearconsole(ctx):
    await ctx.message.delete()
    Clear()
    new_splash()

@bot.command()
@commands.has_any_role(owner, admin, botowner) 
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
    logchannel = bot.get_channel(1063815239059124264)
    await logchannel.send(embed=embed)
    await ctx.message.delete()
    print("Command Executed")

@bot.command()
@commands.has_any_role(owner, admin, botowner) 
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
    logchannel = bot.get_channel(1063815239059124264)
    await logchannel.send(embed=embed)
    await ctx.message.delete()
    print("Command Executed")

@bot.command()
@commands.has_any_role(owner, mod, admin, botowner) 
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
    logchannel = bot.get_channel(1063815239059124264)
    await logchannel.send(embed=embed)

@bot.command()
async def news(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Update V1.3", description=f"This is the latest news about our bot Update", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Added new commands", value="Including ban, kick etc", inline=False)
    embed.add_field(name="Added new Ids to config", value="Owner ids mod ids etc", inline=False)
    embed.add_field(name="Updates coming soon", value="besure to check out https://egg883.shop", inline=False)
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
    embed = discord.Embed(title="Server Info", description=f"This is info about {guild.name}", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url=f"{guild.icon_url}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}", inline=False)
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}", inline=False)
    embed.add_field(name="Member Count", value=f"{member_count}", inline=False)
    embed.add_field(name="Channel Count", value=f"{channels} Channels {text_channels} Text, {voice_channels} Voice, {categories}", inline=False)
    embed.add_field(name="Server Verification", value=f"{str(ctx.guild.verification_level).upper()}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Info", description=f"This is a information page about my bot", colour=0x007bff)
    embed.set_author(name="Egglington", url="https://egg883.shop", icon_url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774966111285289/as.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1063774865729007616/1063774978018906112/yoshi-wave.gif")
    embed.add_field(name="Total Commands", value = f"{len(bot.commands)}", inline=False)
    embed.add_field(name="Prefix", value=f"{prefix}", inline=False)
    embed.add_field(name="Version", value=f"{version}", inline=False)
    embed.add_field(name="Creator", value="This bot was made by eggs#6666 this is a little project i wanted todo", inline=False)
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

#////////////////////////////////////////////////////////////////////////// 
bot.run(bottoken)