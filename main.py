import aiohttp
import datetime
import time
import io
import json
import os
import discord
from colorama import Fore
import random
import re
from datetime import datetime
import sys
from discord_interactions import *
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext.commands import CommandOnCooldown
from discord.ext.commands.cooldowns import BucketType
from roblox import Client
import asyncio
import requests
from bs4 import BeautifulSoup
import random
from discord_slash.utils import manage_components as components
import urllib
import urllib.request
import datetime
import time
import typing
import sqlite3
#////////////////////////////////////////////////////////////////////////// COLOR DEFINING
client1 = Client()
#////////////////////////////////////////////////////////////////////////// CONFIG DEFINING#
with open('config.json', 'r') as f:
    config = json.load(f)
bottoken = config['bot_token']
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
#////////////////////////////////////////////////////////////////////////// GENERIC SH*T 
embed_color = 0xfcd005
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = prefix, intents=intents, help_command=None)
cmds = {len(bot.commands)}
version = "1.2.2"
slash = SlashCommand(bot, sync_commands=True)
MIN_DATE = datetime.datetime(1970, 1, 1)
githuburl = "https://github.com/egg883/Egglington-Discord-bot"
CHANNEL_ID = config['logs']
allowed_guild_ids = [config['serverid']]
total_members = sum([guild.member_count for guild in bot.guilds])
def restart_bot(): 
  os.execv(sys.executable,sys.argv)
#////////////////////////////////////////////////////////////////////////// EVENT STUFF

def new_splash():
    print(f"""{Fore.GREEN}
 _______   _______   _______  __       __  .__   __.   _______ .___________.  ______   .__   __. 
|   ____| /  _____| /  _____||  |     |  | |  \ |  |  /  _____||           | /  __  \  |  \ |  | 
|  |__   |  |  __  |  |  __  |  |     |  | |   \|  | |  |  __  `---|  |----`|  |  |  | |   \|  |                                        
|   __|  |  | |_ | |  | |_ | |  |     |  | |  . `  | |  | |_ |     |  |     |  |  |  | |  . `  | 
|  |____ |  |__| | |  |__| | |  `----.|  | |  |\   | |  |__| |     |  |     |  `--'  | |  |\   | 
|_______| \______|  \______| |_______||__| |__| \__|  \______|     |__|      \______/  |__| \__|                                                                                                                  
================================================================================================
""")
    print(f'{Fore.GREEN}If you need assistance dont hesitate to join our support server! https://discord.gg/EdfyJ47xYe')
    print(f'{Fore.GREEN}{bot.user.name} is now Listening to {len(bot.guilds)} servers')
    print(f"{Fore.GREEN}{bot.user.name}'s Prefix is /")
    print(f"{Fore.GREEN}Do /help for the help commands")

conn = sqlite3.connect('reputation.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user_reputation (
                  user_id TEXT PRIMARY KEY,
                  reputation INTEGER DEFAULT 1000
               )''')
conn.commit()

conn2 = sqlite3.connect('shop.db')
cursor2 = conn.cursor()
cursor2.execute('''CREATE TABLE IF NOT EXISTS shop (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                price INTEGER,
                quantity INTEGER
                )''')
conn2.commit()

conn3 = sqlite3.connect('inventory.db')
cursor3 = conn.cursor()
cursor3.execute('''CREATE TABLE IF NOT EXISTS user_inventory (
                user_id TEXT,
                item_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES user_reputation (user_id),
                FOREIGN KEY (item_id) REFERENCES shop (id)
                )''')
conn3.commit()

conn_profile = sqlite3.connect('profiles.db')
cursor_profile = conn_profile.cursor()
cursor_profile.execute('''
    CREATE TABLE IF NOT EXISTS user_profile (
        user_id TEXT PRIMARY KEY,
        profile_icon TEXT,
        username TEXT,
        bio TEXT
    )
''')
conn_profile.commit()

verified_roles = {}

@bot.event
async def on_member_join(member):
    user_id = str(member.id)
    cursor.execute("SELECT received_coins FROM user_join WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if not result or not result[0]:
        cursor.execute("INSERT OR REPLACE INTO user_join (user_id, received_coins) VALUES (?, 1)", (user_id,))
        conn.commit()
        print(f"gave {member} coins")

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
        embed = discord.Embed(title="Role Update", description=f"{after.mention} was given the following roles: {added_roles_str}", color=0x19AC00)
        await log(embed)

    if removed_roles:
        removed_roles_str = ", ".join(role.name for role in removed_roles)
        embed = discord.Embed(title="Role Update", description=f"{after.mention} had the following roles removed: {removed_roles_str}", color=discord.Color.red())
        await log(embed)

cooldowns = {}

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
        f"Listening on {len(bot.guilds)} servers.",
        f"Still need help? do /help for more help!",
        f"Total Users: {formatted_total}",
    ]
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(10)


bot.loop.create_task(ch_pr())
start_time = time.time()

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
    help_pages = [
        {
            "title": "Help Panel 1/2",
            "description": "This is the Help Panel. Below are commands:",
            "thumbnail_url": "https://i.imgur.com/dSMCKNx.gif",
            "fields": [
                {"name": "🔰 General", "value": "`/whois`, `/yt`, `/vote`, `/choose`, `/poll`", "inline": False},
                {"name": "💥 Fun", "value": "`/coinflip`, `/rps`, `/dice`, `/pp`, `/8ball`", "inline": False},
                {"name": "🛡️ Moderation", "value": "`/kick`, `/ban`, `/unban`, `/purge`, `/mute`, `/unmute`, `/lock`, `/unlock`, `/slowmode`", "inline": False},
                {"name": "🤖 Server", "value": "`/role`, `/deleterole`, `/first`, `/spfp`, `/avatar`, `/afk`, `/setup`, `/balance`, `/resetcoins`,, `/supportchan`", "inline": False},
                {"name": "💰 Economy", "value":"`/daily`, `/bet`, `/slot`, `/additem`, `/buy`, `/deleteitem`, `/remove_balance`, `/profile`, `/setprofile`, `/seteveryonebalance`, `/balance`, `/resetcoins`, `/leaderboard`, `/addcoins`, `/beg`, `/inventory`, `/shop`, `/sell`, `/pay`", "inline": False},
                {"name": "https://eggbot.site", "value": " ", "inline": True}
            ]
        },
        {
            "title": "Help Panel 2/2",
            "description": "This is the second page of the Help Panel.",
            "thumbnail_url": "https://i.imgur.com/dSMCKNx.gif",
            "fields": [
                {"name": "⚙️ Utility", "value": "`/ping`, `/help`, `/invite`, `/sinfo`, `/whois`, `/info`, `/newticket`, `/closeticket`, `/support`, `/uptime`", "inline": False},
                {"name": "👽 Memes", "value": "`/jail`, `/wasted`, `/horny`, `/lolice`, `/pixel`, `/clyde`, `/trump`, `/change`, `/deepfry`", "inline": False},
                {"name": "🎮 Roblox", "value": "`/rgame`, `/ruser`, `/routfit`, `{prefix}rvalue`, `/ruserhis`, `/template`", "inline": False},
                {"name": "⛏️ Minecraft", "value": "`/migrator`, `/vanilla`, `/minecon`, `/realmsmapmaker`, `/mojang`, `/mojangstudios`, `/translator`, `/cobalt`, `/scrolls`, `/turtle`, `/valentine`, `/birthday`, `/dB`, `/Prismarine`, `/snowman`, `/spade`", "inline": False},
                {"name": "https://eggbot.site", "value": " ", "inline": True}
            ]
        }
    ]
    current_page = 0
    message = await ctx.send(embed=get_help_embed(help_pages[current_page]))
    reactions = ["⬅️", "➡️"]
    for reaction in reactions:
        await message.add_reaction(reaction)
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reactions
    while True:
        try:
            reaction, _ = await bot.wait_for("reaction_add", timeout=30, check=check)
            await message.remove_reaction(reaction, ctx.author)

            if str(reaction.emoji) == "⬅️":
                current_page = (current_page - 1) % len(help_pages)
            elif str(reaction.emoji) == "➡️":
                current_page = (current_page + 1) % len(help_pages)
            await message.edit(embed=get_help_embed(help_pages[current_page]))

        except TimeoutError:
            break

def get_help_embed(page):
    embed = discord.Embed(title=page["title"], description=page["description"], color=0x19AC00)
    embed.set_thumbnail(url=page["thumbnail_url"])
    for field in page["fields"]:
        embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
    return embed

@slash.slash(name="uptime", description="Get the uptime of the bot.")
async def uptime(ctx: SlashContext):
    embed=discord.Embed(title="Uptime", url="https://eggbot.site", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name="Uptime", value=f"{str(datetime.timedelta(seconds=round(time.time() - start_time)))}", inline=False)
    await ctx.send(embed=embed)
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
    embed=discord.Embed(title="Slowmode command", url="https://eggbot.site", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="Slowmode set to:", value=f"{seconds} seconds", inline=False)
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
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
    embed=discord.Embed(title="Lock command", url="https://eggbot.site", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="Channel locked", value=f"{ctx.channel.mention}", inline=False)
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
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
    embed=discord.Embed(title="Unlock command", url="https://eggbot.site", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="Channel unlocked", value=f"{ctx.channel.mention}", inline=False)
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
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
    embed=discord.Embed(title="Purge command", url="https://eggbot.site", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="Purged", value=f"I have purged {limit} messages.")
    await ctx.send(embed=embed,delete_after=config['deletetime'])

afk_users = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author == bot.user:
        return
    for user in message.mentions:
        if user.nick is not None and user.nick.startswith('[AFK]'):
            if 'is now AFK' in user.nick:
                afk_message = 'is now AFK'
            else:
                afk_message = user.nick.split(': ')[-1]
            await message.channel.send(f"{message.author.mention} {user.mention} is currently AFK. For {afk_message}")
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
    for mention in message.mentions:
        if mention.nick is not None and mention.nick.startswith('[AFK]'):
            user = mention
            if 'is now AFK' in user.nick:
                afk_message = 'No reason provided'
            else:
                afk_message = user.nick.split(': ')[-1]
            await message.channel.send(f"{message.author.mention} {user.mention} is currently AFK.")
            break

    if message.author.nick is not None and message.author.nick.startswith('[AFK]'):
        user = message.author
        await user.edit(nick=user.display_name.replace('[AFK]', ''))
        await message.channel.send(f"{user.mention} is back from AFK")

    await bot.process_commands(message)

@slash.slash(name="avatar", description="Get the avatar of a user.")
async def avatar(ctx: SlashContext, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"{member.name}'s avatar", color=0x19AC00)
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
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
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
    embed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted ", colour=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url=f"https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed,delete_after=config['deletetime'])
    await member.remove_roles(mutedRole, reason=reason)
    await member.send(f" You have been unmuted in: {guild.name} reason: {reason}")

#thx tyris for this

@slash.slash(name="template", description="steals shirt template by ID", options=[
    {
        "name": "id",
        "description": "The ID of the shirt asset",
        "type": SlashCommandOptionType.STRING,
        "required": True
    }
])
async def get_shirt(ctx: SlashContext, id: str):
    assetRequest = requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={id}", allow_redirects=False)
    assetLocation = assetRequest.headers["location"]
    locationRequest = requests.get(assetLocation)
    templateAssetId = re.search(r"\?id=(\d+)", str(locationRequest.content)).group()[4:]
    templateDownloadRequest = requests.get(f"https://assetdelivery.roblox.com/v1/asset/?id={templateAssetId}", allow_redirects=False)
    templateBinaryRequest = requests.get(templateDownloadRequest.headers["location"])
    with open("shirt.png", "wb") as shirt:
        shirt.write(templateBinaryRequest.content)
    await ctx.send(file=discord.File("shirt.png"))


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
    embed = discord.Embed(title=f"Info about **{member.display_name}**", colour=0x19AC00)
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"Egglington", url="https://eggbot.site", icon_url=f"https://i.imgur.com/qrogvhd.png")
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
        embed = discord.Embed(title="Created Role", colour=0x19AC00)
        embed.set_author(name=f"Egglington", url="https://eggbot.site", icon_url=f"https://i.imgur.com/qrogvhd.png")
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
    embed = discord.Embed(title=F"PP command executed!", url="https://eggbot.site", colour=0x19AC00)
    embed.set_author(name=f"Egglington", url="https://eggbot.site", icon_url=f"https://i.imgur.com/qrogvhd.png")
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
        embed = discord.Embed(title="Unbanned", description=f"{member_obj.mention} was unbanned", colour=0x19AC00)
    except discord.errors.NotFound:
        await guild.unban(discord.Object(id=int(member)))
        embed = discord.Embed(title="Unbanned", description=f"User with ID {member} was unbanned", colour=0x19AC00)

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
    embed=discord.Embed(title="Command Executed", colour=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/RhaVXcL.gif")
    embed.add_field(name="**Please Wait**", value="Bot Is Restarting.", inline=False)
    await ctx.send(embed=embed, delete_after=deletein)
    print("restarting bot")
    restart_bot()


@slash.slash(name="sinfo", description="Get information about the server")
async def sinfo(ctx):
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    guild = ctx.guild
    categories = len(ctx.guild.categories)
    member_count = len(ctx.guild.members)
    channels = text_channels + voice_channels
    embed = discord.Embed(title="Server Info", description=f"This is info about **{guild.name}**", colour=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url=f"{guild.icon_url}")
    embed.add_field(name="Server ID", value=f"```{ctx.guild.id}```", inline=False)
    embed.add_field(name="Channel Count", value=f"```{channels} Channels {text_channels} Text, {voice_channels} Voice, {categories}```", inline=False)
    embed.add_field(name="Server Owner", value=f"```{ctx.guild.owner}```", inline=True)
    embed.add_field(name="Member Count", value=f"```{member_count}```", inline=True)
    embed.add_field(name="Server Verification", value=f"```{str(ctx.guild.verification_level).upper()}```", inline=False)
    await ctx.send(embed=embed)

@slash.slash(
    name="sell",
    description="Sell an item from your inventory",
    options=[
        create_option(
            name="item_name",
            description="Name of the item to sell",
            option_type=3,
            required=True
        )
    ]
)
async def sell_item(ctx: SlashContext, item_name: str):
    user_id = str(ctx.author.id)
    cursor2.execute("SELECT id, price FROM shop WHERE name = ?", (item_name,))
    item_data = cursor2.fetchone()
    if not item_data:
        await ctx.send(f"The item '{item_name}' does not exist in the shop.")
        return
    item_id, item_price = item_data
    cursor3.execute("SELECT item_id FROM user_inventory WHERE user_id = ? AND item_id = ?", (user_id, item_id))
    user_has_item = cursor3.fetchone()
    if not user_has_item:
        await ctx.send(f"You don't have the item '{item_name}' in your inventory.")
        return
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    user_balance = cursor.fetchone()[0]
    selling_price = item_price // 2
    user_balance += selling_price
    cursor.execute("UPDATE user_reputation SET reputation = ? WHERE user_id = ?", (user_balance, user_id))
    cursor3.execute("DELETE FROM user_inventory WHERE rowid IN (SELECT rowid FROM user_inventory WHERE user_id = ? AND item_id = ? LIMIT 1)", (user_id, item_id))
    conn.commit()
    await ctx.send(f"You have sold one item of '{item_name}' for {selling_price} EggCoins. Your new balance is {user_balance}.")


@slash.slash(name="info", description="Displays info about the bot.")
async def info(ctx):
    total = 0
    for guild in bot.guilds:
        total += guild.member_count
    formatted_total = '{:,}'.format(total)
    embed=discord.Embed(title="Info Panel", color=0x19AC00)
    embed.set_thumbnail(url= "https://i.imgur.com/dSMCKNx.gif")
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="About Egglington:", value=f"Egglington is a multi-purpose discord bot developed by Jack (egg883), It is an open source project on Github that you can easily host yourself. Egglington is a easy to use bot for many things, roblox, minecraft, moderation, memes anything egglington is fun to use with its economy commands for extra fun.", inline=False)
    embed.add_field(name="Total Commands:", value=f"{len(slash.commands)}", inline=True)
    embed.add_field(name="Prefix:", value=f"[{prefix}] [/]", inline=True)
    embed.add_field(name="Version:", value=f"{version}", inline=True)
    embed.add_field(name="Total Members:", value=f"{formatted_total}", inline=True)
    embed.add_field(name="Total Servers:", value=f"{len(bot.guilds)}", inline=True)
    embed.add_field(name="Github:", value=f"Click [here](https://github.com/egg883/Egglington-Discord-bot)", inline=True)
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="first", description="Displays the first message ever sent in the channel.")
async def first(ctx):
    await ctx.defer()
    channel = ctx.channel
    first_message = (await channel.history(limit = 1, oldest_first = True).flatten())[0]
    embed = discord.Embed(title="First message", description=f"This is the first ever message sent in this channel", colour=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.add_field(name="First Message Content", value = f"{first_message.content}", inline=False)
    embed.add_field(name="First Message link", value = f"{first_message.jump_url}", inline=False)
    await ctx.send(embed=embed)


@slash.slash(
    name="setup",
    description="Set up verification",
    options=[
        {
            "name": "verification_channel",
            "description": "Select the verification channel",
            "type": SlashCommandOptionType.CHANNEL,
            "required": True,
        },
        {
            "name": "verified_role",
            "description": "Select the verified role",
            "type": SlashCommandOptionType.ROLE,
            "required": True,
        }
    ],
)
async def setup(ctx: SlashContext, verification_channel: discord.TextChannel, verified_role: discord.Role):
    if ctx.author.guild_permissions.administrator:
        verified_roles[ctx.guild.id] = verified_role
        embed = discord.Embed(title=f"Verification Setup for {ctx.guild.name}",description=f"Type `/verify` to verify for **{ctx.guild.name}**.", color=0x19AC00,)
        embed.add_field(name="You must read rules before entering", value=f"Make sure to read the rules before typing `/verify`")
        embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
        await verification_channel.send(embed=embed)
        await ctx.send(content=f"Verification setup message sent to {verification_channel.mention}.", hidden=True)
    else:
        await ctx.send(content="You must have administrator permissions to set up verification.", hidden=True)

@slash.slash(name="verify", description="Verify yourself")
async def verify(ctx: SlashContext):
    if ctx.guild.id in verified_roles:
        verified_role = verified_roles[ctx.guild.id]
        if verified_role not in ctx.author.roles:
            await ctx.author.add_roles(verified_role)
            await ctx.send(content="You are now verified!", hidden=True)
        else:
            await ctx.send(content="You are already verified!", hidden=True)
    else:
        await ctx.send(content="Verification role is not set up for this server. Please run `/setup` first.", hidden=True)


@slash.slash(name="spfp", description="Displays the server icon.")
async def spfp(ctx):
    await ctx.defer()
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}'s Server Icon", colour=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_image(url=f"{guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
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
        embed=discord.Embed(title=f"Found Info for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
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
        embed.set_footer(text=f"{username}'s Information", icon_url= "https://i.imgur.com/BcCoAWb.png")
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
        embed=discord.Embed(title=f"Found current outfit for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name=f"Username:", value=f"{user.name}", inline=False)
        embed.set_image(url = f"{user_thumbnail.image_url}")
        embed.set_footer(text=f"{username}'s current outfit", icon_url= "https://i.imgur.com/BcCoAWb.png")
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
                          color=0x19AC00)
    embed.set_author(name="Egglington",
                     url="https://eggbot.site",
                     icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site",
                     icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_image(url=stuff['message'])
    await ctx.send(embed=embed)

@slash.slash(name="change",
             description="Generates a Image based on your specification")
async def _changemymind(ctx, msg: str):
    response = requests.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={msg}")
    stuff = json.loads(response.text)
    embed = discord.Embed(title="Meanwhile In London:",
                          color=0x19AC00)
    embed.set_author(name="Egglington",
                     url="https://eggbot.site",
                     icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site",
                     icon_url="https://i.imgur.com/qrogvhd.png")
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
    embed=discord.Embed(title="Clyde has a message for you", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
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
        embed=discord.Embed(title=f"Past usernames for {user.name} ", url=f"https://www.roblox.com/users/{user.id}/profile", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.set_thumbnail(url=f"{user_thumbnail.image_url}")
        embed.add_field(name=f"Past usernames", value=f"```{users}```", inline=False)
        embed.set_footer(text=f"{username}'s Past Usernames", icon_url= "https://i.imgur.com/BcCoAWb.png")
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
    embed=discord.Embed(title=f"Rolimons Info for {user.name} ", url=f"https://www.rolimons.com/player/{userid}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
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
    embed.set_footer(text=f"{username}'s rolimons", icon_url= "https://i.imgur.com/RmEitTn.png")
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
    embed=discord.Embed(title=f"Game info for {name} ", url=f"{url}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url=f"https://i.imgur.com/BcCoAWb.png")
    embed.add_field(name=f"visits:", value=f"```{visit}```", inline=True)
    embed.add_field(name=f"favorites:", value=f"```{fav}```", inline=True)
    embed.add_field(name=f"player count:", value=f"```{player}```", inline=True)
    embed.add_field(name=f"Server Size:", value=f"```{size}```", inline=True)
    embed.add_field(name=f"Created:", value=f"```{created}```", inline=True)
    embed.add_field(name=f"Last Updated:", value=f"```{updated}```", inline=True)
    embed.set_footer(text=f"{name}'s Info", icon_url= "https://i.imgur.com/BcCoAWb.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@_changemymind.error
async def changemymind(ctx,error):
    embed=discord.Embed(title="COMMAND ERROR", color=0xFF0400)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="Required Field is too long", value=f"Try shortening your reponse", inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/DyHqR2S.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@restart.error
async def restart(ctx,error):
    embed=discord.Embed(title="RESTART COMMAND ERROR", color=0xFF0400)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.add_field(name="bot Owner Only Command", value=f"You must be the bot owner to use command.", inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/DyHqR2S.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, delete_after=deletein)

@bot.event
async def on_command_error(ctx, error:commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
            cmd = ctx.message.content.split()[0]
            cmd = cmd.lstrip(prefix)
            embed=discord.Embed(title="COMMAND ERROR", color=0xFF0400)
            embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
            embed.add_field(name="COMMAND NOT FOUND", value=f"The command {cmd} does not exist", inline=True)
            embed.set_thumbnail(url="https://i.imgur.com/DyHqR2S.png")
            embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
            embed.timestamp = datetime.datetime.utcnow()
            print(Fore.RED+f"[ERR] The Command {cmd} Does not exist"+Fore.RESET)
            await ctx.send(embed=embed, delete_after=30)
tickets = {}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    if payload.message_id in tickets and payload.emoji.name == '🎫':
        ticket_data = tickets[payload.message_id]
        user = bot.get_user(payload.user_id)
        guild = bot.get_guild(payload.guild_id)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
        }
        support_role = discord.utils.get(guild.roles, name="Support Team")
        if not support_role:
            support_role = await guild.create_role(name="Support Team")

        overwrites[support_role] = discord.PermissionOverwrite(read_messages=True)

        ticket_channel = await guild.create_text_channel(name=f'ticket-{user.display_name}', overwrites=overwrites)
        await ticket_channel.send(f"Support Ticket for {user.mention} - React with 📥 to close this ticket.")
        await ticket_channel.send(f"{user.mention} Please describe your issue here.")
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction('🎫', user)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return
    if payload.message_id in tickets and payload.emoji.name == '🎫':
        ticket_data = tickets[payload.message_id]
        user = bot.get_user(payload.user_id)
        guild = bot.get_guild(payload.guild_id)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
        }
        support_role = discord.utils.get(guild.roles, name="Support Team")
        if not support_role:
            support_role = await guild.create_role(name="Support Team")

        overwrites[support_role] = discord.PermissionOverwrite(read_messages=True)

        ticket_channel = await guild.create_text_channel(name=f'ticket-{user.display_name}', overwrites=overwrites)
        await ticket_channel.send(f"Support Ticket for {user.mention} ")
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction('🎫', user)

@slash.slash(
    name="supportchan",
    description="Open a support ticket",
    options=[
        {
            "name": "support_channel",
            "description": "Select a support channel",
            "type": 7,
            "required": True
        }
    ]
)
async def supportchan(ctx: SlashContext, support_channel: discord.TextChannel):
    support_embed = discord.Embed(
        title="Support Ticket",
        description="Click the 🎫 emoji below to open a support ticket.",
        color=0x19AC00
    )
    support_message = await support_channel.send(embed=support_embed)
    await support_message.add_reaction('🎫')
    tickets[support_message.id] = {}

@slash.slash(
    name="closeticket",
    description="Close the current support ticket",
)
async def close_ticket(ctx: SlashContext):
    message_id = ctx.channel.last_message_id
    if message_id in tickets and tickets[message_id]["user"] == ctx.author:
        await ctx.send(f'Ticket closed by {ctx.author.mention}')
        await tickets[message_id]["channel"].delete()
        del tickets[message_id]
    else:
        await ctx.send("You don't have an open support ticket.")

@slash.slash(name="ping", description="Check bot latency.")
async def ping(ctx: SlashContext):
    embed = discord.Embed(title="Pong!", description=f"Latency: {round(bot.latency * 1000)}ms", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="invite", description="Invite the bot to your server.")
async def invite(ctx: SlashContext):
    embed = discord.Embed(title="Invite Egglington", description="Click [here](https://discord.com/api/oauth2/authorize?client_id=1063758752160960573&permissions=8&scope=bot%20applications.commands) to invite the bot to your server.", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="support", description="Join the support server.")
async def support(ctx: SlashContext):
    embed = discord.Embed(title="Support Server", description="Click [here](https://discord.gg/EdfyJ47xYe) to join the support server.", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="vote", description="Vote for the bot.")
async def vote(ctx: SlashContext):
    embed = discord.Embed(title="Vote for Egglington", description="Click [here](https://top.gg/bot/1063758752160960573/vote) to vote for the bot.", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="github", description="View the bot's source code.")
async def github(ctx: SlashContext):
    embed = discord.Embed(title="Egglington's GitHub", description="Click [here](https://github.com/egg883/Egglington-Discord-bot) to view the bot's source code.", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

symb = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎"]

@slash.slash(
    name="slot",
    description="Spin a slot",
)
async def slot(ctx: SlashContext):
    user_id = str(ctx.author.id)
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if not result:
        await ctx.send("You don't have any EggCoins yet.")
        return
    reputation = result[0]
    if reputation < 450:
        await ctx.send("You need at least 450 EggCoins to play the slot machine.")
        return
    is_winning = random.random() <= 0.23
    cursor.execute("UPDATE user_reputation SET reputation = reputation - 10 WHERE user_id = ?", (user_id,))
    conn.commit()
    if is_winning:
        reputation_change = random.randint(2000, 8000)
    else:
        reputation_change = -450

    cursor.execute("UPDATE user_reputation SET reputation = reputation + ? WHERE user_id = ?", (reputation_change, user_id))
    conn.commit()

    resp = f"{ctx.author.mention} spun the slot machine:\n\n"
    resp += " ".join(random.choice(symb) for _ in range(3))

    if is_winning:
        resp += f"\n\nYou Won The Jackpot! 🎉 +{reputation_change} EggCoins"
    else:
        resp += f"\n\nYou failed {reputation_change} EggCoins"
    
    await ctx.send(resp)


@slash.slash(
    name="beg",
    description="beg for eggcoins",
)
async def beg(ctx: commands.Context):
    if ctx.author.id in cooldowns:
        await ctx.send(f"You are on cooldown. Try again in {cooldowns[ctx.author.id]:.2f} seconds.")
    else:
        failure_chance = random.random()
        if failure_chance <= 0.45:
            await ctx.send("You begged, but no one was generous enough to give you eggcoins this time.")
        else:
            reputation_change = random.randint(35, 250)
            user_id = str(ctx.author.id)
            cursor.execute("UPDATE user_reputation SET reputation = reputation + ? WHERE user_id = ?", (reputation_change, user_id,))
            conn.commit()
            await ctx.send(f"You begged and received {reputation_change} eggcoins!")
            cooldowns[ctx.author.id] = 30.0
            await asyncio.sleep(30)
            del cooldowns[ctx.author.id]

@slash.slash(
    name="leaderboard",
    description="Show the top EggCoins users",
)
async def leaderboard(ctx: commands.Context):
    cursor.execute("SELECT user_id, reputation FROM user_reputation ORDER BY reputation DESC LIMIT 10")
    top_users = cursor.fetchall()
    if top_users:
        resp = "**Top 10 Users with the Most EggCoins:**\n"
        for index, (user_id, reputation) in enumerate(top_users, start=1):
            user = ctx.guild.get_member(int(user_id))
            if user:
                resp += f"{index}. {user.display_name} - EggCoins: {reputation}\n"
            else:
                resp += f"{index}. Unknown User - EggCoins: {reputation}\n"
    else:
        resp = "No users found on the leaderboard."
    
    await ctx.send(resp)

@slash.slash(
    name="additem",
    description="Add an item to the shop",
    options=[
        {
            "name": "name",
            "description": "Item name",
            "type": 3,
            "required": True
        },
        {
            "name": "description",
            "description": "Item description",
            "type": 3,
            "required": True
        },
        {
            "name": "price",
            "description": "Item price",
            "type": 4,
            "required": True
        }
    ]
)
async def add_item(ctx: SlashContext, name: str, description: str, price: int):
    if ctx.author.id == botowner:
        cursor.execute('INSERT INTO shop (name, description, price) VALUES (?, ?, ?)', (name, description, price))
        conn.commit()
        await ctx.send(f"Item added to the shop: {name} - {description} - Price: {price}")
    else:
        await ctx.send("Only the bot owner can use this command.")

@slash.slash(
    name="buy",
    description="Buy an item from the shop",
    options=[
        {
            "name": "item_name",
            "description": "Name of the item you want to buy",
            "type": 3,
            "required": True
        }
    ]
)
async def buy_item(ctx: SlashContext, item_name: str):
    user_id = str(ctx.author.id)
    cursor.execute('SELECT id, name, description, price FROM shop WHERE name = ?', (item_name,))
    item = cursor.fetchone()

    if item:
        item_id, item_name, item_description, item_price = item
        item_price = int(item_price)
        cursor.execute('SELECT reputation FROM user_reputation WHERE user_id = ?', (user_id,))
        user_balance = cursor.fetchone()
        
        if user_balance:
            user_balance = int(user_balance[0])
            if user_balance >= item_price:
                cursor.execute('UPDATE user_reputation SET reputation = reputation - ? WHERE user_id = ?', (item_price, user_id))
                cursor.execute('INSERT INTO user_inventory (user_id, item_id) VALUES (?, ?)', (user_id, item_id))
                conn.commit()

                await ctx.send(f"You've purchased {item_name} - {item_description} for {item_price} balance.")
            else:
                await ctx.send("You don't have enough balance to buy this item.")
        else:
            await ctx.send("You don't have a balance. Please earn reputation first.")
    else:
        await ctx.send(f"Item '{item_name}' not found in the shop.")

@slash.slash(
    name="inventory",
    description="View your inventory"
)
async def view_inventory(ctx: SlashContext):
    user_id = str(ctx.author.id)
    cursor.execute('''
        SELECT shop.name, shop.description, shop.price, COUNT(user_inventory.item_id)
        FROM user_inventory
        INNER JOIN shop ON user_inventory.item_id = shop.id
        WHERE user_id = ?
        GROUP BY user_inventory.item_id, shop.name, shop.description, shop.price
    ''', (user_id,))
    items = cursor.fetchall()

    total_value = 0

    if not items:
        await ctx.send("Your inventory is currently empty.")
    else:
        paginated_embeds = []
        current_page = 1

        for (name, description, price, quantity) in items:
            item_value = price * quantity
            total_value += item_value

        current_embed = discord.Embed(
            title="Your Inventory",
            description=f"Total Value: {total_value} eggcoins",
            color=0x00FF00
        )
        current_embed.set_thumbnail(url="https://images.vexels.com/media/users/3/152838/isolated/preview/2c1e567e0df96c142a12dec74c0eb314-school-backpack-flat-icon-by-vexels.png")

        current_embed.set_footer(text=f"Page {current_page}")

        for (name, description, price, quantity) in items:
            if quantity > 1:
                name = f"{name} (x{quantity})"
            current_embed.add_field(name=name, value=description, inline=False)

            if len(current_embed.fields) == 10:
                paginated_embeds.append(current_embed)
                current_page += 1
                current_embed = discord.Embed(
                    title="Your Inventory",
                    color=0x00FF00
                )
                current_embed.set_thumbnail(url="https://images.vexels.com/media/users/3/152838/isolated/preview/2c1e567e0df96c142a12dec74c0eb314-school-backpack-flat-icon-by-vexels.png")

                current_embed.set_footer(text=f"Page {current_page}")

        if len(current_embed.fields) > 0:
            paginated_embeds.append(current_embed)

        current_page = 0
        msg = await ctx.send(embed=paginated_embeds[current_page])

        reactions = ['⬅️', '➡️']

        for reaction in reactions:
            await msg.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions

        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)
                if str(reaction.emoji) == '➡️' and current_page < len(paginated_embeds) - 1:
                    current_page += 1
                elif str(reaction.emoji) == '⬅️' and current_page > 0:
                    current_page -= 1

                await msg.edit(embed=paginated_embeds[current_page])
                await msg.remove_reaction(reaction, user)

            except TimeoutError:
                break

        await msg.clear_reactions()

@slash.slash(
    name="deleteitem",
    description="Delete an item from the shop",
    options=[
        create_option(
            name="item_name",
            description="Name of the item to delete",
            option_type=3,
            required=True
        )
    ]
)
async def delete_item(ctx: SlashContext, item_name: str):
    if ctx.author.id != botowner:
        await ctx.send("You do not have permission to delete items from the shop.")
        return
    cursor.execute('SELECT * FROM shop WHERE name = ?', (item_name,))
    item = cursor.fetchone()

    if not item:
        await ctx.send(f"The item with the name '{item_name}' does not exist in the shop.")
        return
    cursor.execute('DELETE FROM shop WHERE name = ?', (item_name,))
    conn.commit()

    await ctx.send(f"Item with the name '{item_name}' has been successfully deleted from the shop.")

@slash.slash(
    name="setprofile",
    description="Set your profile data",
    options=[
        create_option(
            name="profile_icon",
            description="Profile icon URL",
            option_type=3, 
            required=True
        ),
        create_option(
            name="username",
            description="Your username",
            option_type=3,
            required=True
        ),
        create_option(
            name="bio",
            description="Your bio",
            option_type=3,
            required=True
        )
    ]
)
async def set_profile(ctx: SlashContext, profile_icon: str, username: str, bio: str):
    user_id = str(ctx.author.id)
    cursor_profile.execute('SELECT * FROM user_profile WHERE user_id = ?', (user_id,))
    existing_profile = cursor_profile.fetchone()

    if existing_profile:
        cursor_profile.execute('''
            UPDATE user_profile
            SET profile_icon = ?, username = ?, bio = ?
            WHERE user_id = ?
        ''', (profile_icon, username, bio, user_id))
    else:
        cursor_profile.execute('''
            INSERT INTO user_profile (user_id, profile_icon, username, bio)
            VALUES (?, ?, ?, ?)
        ''', (user_id, profile_icon, username, bio))

    conn_profile.commit()

    await ctx.send("Your profile has been updated.")

@slash.slash(
    name="profile",
    description="View a user's profile",
    options=[
        create_option(
            name="user",
            description="User to view the profile of",
            option_type=6,
            required=False
        )
    ]
)
async def view_profile(ctx: SlashContext, user: discord.User = None):
    if user is None:
        user = ctx.author
    user_id = str(user.id)
    cursor_profile.execute('SELECT profile_icon, username, bio FROM user_profile WHERE user_id = ?', (user_id,))
    profile_data = cursor_profile.fetchone()

    if not profile_data:
        await ctx.send(f"{user.display_name} hasn't set up a profile yet.")
        return

    profile_icon, username, bio = profile_data
    is_bot_owner = user.id == botowner
    if is_bot_owner:
        username += " 🛡️"

    cursor.execute('''
        SELECT shop.name, shop.price, COUNT(user_inventory.item_id)
        FROM user_inventory
        INNER JOIN shop ON user_inventory.item_id = shop.id
        WHERE user_id = ?
        GROUP BY user_inventory.item_id, shop.name, shop.price
    ''', (user_id,))
    items = cursor.fetchall()
    total_item_count = sum(quantity for (_, _, quantity) in items)
    total_item_value = sum(price * quantity for (_, price, quantity) in items)

    cursor.execute('SELECT reputation FROM user_reputation WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
    else:
        balance = 0

    member_since = user.created_at.strftime('%B %d, %Y')

    embed = discord.Embed(
        title=f"{username} 🌟",
        description=f"{bio} 📝",
        color=0x00FF00
    )
    embed.set_thumbnail(url=profile_icon)
    embed.add_field(name="Total Item Count", value=f"{total_item_count} 🛒", inline=True)
    embed.add_field(name="Total Item Value", value=f"{total_item_value} 💰", inline=True)
    embed.add_field(name="Balance", value=f"{balance} 💳", inline=True)
    embed.add_field(name="Member Since", value=f"{member_since} ⌛", inline=False)
    await ctx.send(embed=embed)

@slash.slash(
    name="shop",
    description="List items in the shop"
)
async def list_shop(ctx: SlashContext):
    cursor.execute('SELECT name, description, price FROM shop')
    items = cursor.fetchall()

    if not items:
        await ctx.send("The shop is currently empty.")
        return

    items_per_page = 9
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    current_page = 0

    thumbnail_url = "https://cdn0.iconfinder.com/data/icons/shopping-set-3/512/e7-256.png"

    def generate_embed(page):
        start_idx = page * items_per_page
        end_idx = (page + 1) * items_per_page
        page_items = items[start_idx:end_idx]

        embed = discord.Embed(
            title=f"Shop Items (Page {page + 1}/{total_pages})",
            color=0x00FF00
        )
        embed.set_thumbnail(url=thumbnail_url)

        for (name, description, price) in page_items:
            embed.add_field(name=name, value=f"{description}\nPrice: {price}", inline=True)
        return embed

    message = await ctx.send(embed=generate_embed(current_page))
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

    while True:
        try:
            reaction, user = await ctx.bot.wait_for("reaction_add", check=check, timeout=60)
            if str(reaction.emoji) == "➡️" and current_page < total_pages - 1:
                current_page += 1
                await message.edit(embed=generate_embed(current_page))
            elif str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
                await message.edit(embed=generate_embed(current_page))
            await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break

@slash.slash(
    name="pay",
    description="Pay EggCoins to another user",
    options=[
        create_option(
            name="recipient",
            description="User to pay",
            option_type=6,
            required=True
        ),
        create_option(
            name="amount",
            description="Amount of EggCoins to pay",
            option_type=4,
            required=True
        )
    ]
)
@commands.cooldown(1, 30, BucketType.user)
async def pay(ctx: SlashContext, recipient: discord.User, amount: int):
    user_id = str(ctx.author.id)
    recipient_id = str(recipient.id)
    if amount <= 0:
        await ctx.send("Please enter a valid amount of EggCoins to pay.")
        return
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    sender_data = cursor.fetchone()
    if not sender_data:
        await ctx.send("You don't have any EggCoins to pay.")
        return
    sender_balance = sender_data[0]
    if sender_balance < amount:
        await ctx.send("You don't have enough EggCoins to make this payment.")
        return
    cursor.execute("UPDATE user_reputation SET reputation = reputation - ? WHERE user_id = ?", (amount, user_id))
    cursor.execute("INSERT OR IGNORE INTO user_reputation (user_id, reputation) VALUES (?, 0)", (recipient_id,))
    cursor.execute("UPDATE user_reputation SET reputation = reputation + ? WHERE user_id = ?", (amount, recipient_id))
    conn.commit()
    recipient_dm = await recipient.create_dm()
    await recipient_dm.send(f"You've received {amount} EggCoins from {ctx.author.display_name}.")
    await ctx.send(f"You have paid {amount} EggCoins to {recipient.display_name}. Your new balance is {sender_balance - amount}.")

@pay.error
async def pay_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.0f} seconds.")


@slash.slash(
    name="balance",
    description="Check your EggCoins",
)
async def balance(ctx: commands.Context):
    user_id = str(ctx.author.id)
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        reputation = result[0]
        if reputation == 0:
            cursor.execute("UPDATE user_reputation SET reputation = 10 WHERE user_id = ?", (user_id,))
            conn.commit()
            resp = f"{ctx.author.mention}, Seems you are broke, Here take 10 EggCoins."
        else:
            resp = f"{ctx.author.mention}, your balance is {reputation}."
    else:
        resp = f"{ctx.author.mention}, you don't have any EggCoins yet."

    await ctx.send(resp)

@slash.slash(
    name="remove_balance",
    description="Remove EggCoins from a user",
    options=[
        create_option(
            name="user",
            description="User to remove EggCoins from",
            option_type=6,
            required=True
        ),
        create_option(
            name="amount",
            description="Amount of EggCoins to remove",
            option_type=4,
            required=True
        )
    ]
)
async def remove_balance(ctx: SlashContext, user: discord.User, amount: int):
    if ctx.author.id != botowner:
        await ctx.send("You do not have permission to remove balance.")
        return

    user_id = str(user.id)
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        current_balance = result[0]
        
        if current_balance >= amount:
            new_balance = max(current_balance - amount, 1)
            cursor.execute("UPDATE user_reputation SET reputation = ? WHERE user_id = ?", (new_balance, user_id))
            conn.commit()
            await ctx.send(f"{user.mention} has had {amount} EggCoins removed. Their new balance is {new_balance}.")
        else:
            await ctx.send(f"{user.mention} does not have enough EggCoins to remove.")
    else:
        await ctx.send(f"{user.mention} does not have any EggCoins to remove.")

@slash.slash(
    name="seteveryonebalance",
    description="Set everyone's balance to 1000 EggCoins",
)
async def set_everyone_balance(ctx: commands.Context):
    if ctx.author.id != botowner:
        await ctx.send("You do not have permission to use this command.")
        return
    guild = ctx.guild
    members = guild.members
    for member in members:
        user_id = str(member.id)
        cursor.execute("INSERT OR REPLACE INTO user_reputation (user_id, reputation) VALUES (?, 1000)", (user_id,))

    conn.commit()
    await ctx.send("All server members now have 1000 EggCoins.")

@slash.slash(
    name="resetcoins",
    description="Reset everyone's coins to default (1000)",
)
async def resetcoins(ctx: commands.Context):
    allowed_user_id = botowner
    if ctx.author.id != allowed_user_id:
        await ctx.send("You are not authorized to use this command.")
        return
    cursor.execute("UPDATE user_reputation SET reputation = 1000")
    conn.commit()
    
    await ctx.send("All user coins have been reset to 1000.")



@slash.slash(
    name="addcoins",
    description="Add eggcoins to a user",
    options=[
        create_option(
            name="user",
            description="User to add eggcoins to",
            option_type=SlashCommandOptionType.USER,
            required=True
        ),
        create_option(
            name="amount",
            description="Amount of eggcoins to add",
            option_type=SlashCommandOptionType.INTEGER,
            required=True
        )
    ]
)
async def add_coins(ctx: commands.Context, user: discord.User, amount: int):
    allowed_user_id = botowner
    if ctx.author.id != allowed_user_id:
        await ctx.send("You are not authorized to use this command.")
        return
    user_id = str(user.id)
    cursor.execute("UPDATE user_reputation SET reputation = reputation + ? WHERE user_id = ?", (amount, user_id,))
    conn.commit()
    await ctx.send(f"eggcoins added! {user.mention} now has {amount} more eggcoins.")

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
        "Very doubtful.",
        "You Smell"
    ]
    embed = discord.Embed(title="8ball", description=f"Question: {question}\nAnswer: {random.choice(responses)}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="coinflip", description="Flip a coin.")
async def coinflip(ctx: SlashContext):
    responses = [
        "Heads",
        "Tails"
    ]
    embed = discord.Embed(title="Coinflip", description=f"{random.choice(responses)}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="rps", description="Play rock paper scissors.")
async def rps(ctx: SlashContext, *, choice):
    responses = [
        "Rock",
        "Paper",
        "Scissors"
    ]
    embed = discord.Embed(title="Rock Paper Scissors", description=f"Your choice: {choice}\nMy choice: {random.choice(responses)}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
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
    embed = discord.Embed(title="Dice", description=f"{random.choice(responses)}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="choose", description="Choose between multiple options.")
async def choose(ctx: SlashContext, *, options):
    embed = discord.Embed(title="Choose", description=f"{random.choice(options.split())}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

@slash.slash(name="poll", description="Create a poll.")
async def poll(ctx: SlashContext, *, question):
    embed = discord.Embed(title="Poll", description=f"{question}", color=0x19AC00)
    embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site", icon_url = "https://i.imgur.com/qrogvhd.png")
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    embed.timestamp = datetime.datetime.utcnow()
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")



@slash.slash(name="Migrator", description="Migrator Cape")
async def mig(ctx: SlashContext):
        embed = discord.Embed(title="Migrator", url="https://namemc.com/cape/8a6cc02cc86e43f1", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="3682264★", inline=False)
        embed.add_field(name= "How To Obtain", value="The Migrator cape in Minecraft is given to players who have migrated their Mojang or legacy account to the new Microsoft account system before December 1, 2020.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/8a6cc02cc86e43f1)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/YqohpU1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Vanilla", description="Vanilla Cape")
async def van(ctx: SlashContext):
        embed = discord.Embed(title="Vanilla", url="https://namemc.com/cape/3c1a1e7e50fce5f0", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="276967★", inline=False)
        embed.add_field(name= "How To Obtain", value="The vanilla cape in Minecraft Java Edition can be obtained by owning both Java Edition and Bedrock Edition in the same Microsoft account before June 6, 2022.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/3c1a1e7e50fce5f0)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/5rl3xVh.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="MineCon2016", description="MineCon 2016 Cape")
async def min016(ctx: SlashContext):
        embed = discord.Embed(title="MineCon 2016", url="https://namemc.com/cape/1981aad373fa9754", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="7268★", inline=False)
        embed.add_field(name= "How To Obtain", value="A redemption link for the cape was emailed to people attending minecon.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/1981aad373fa9754)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/RnqdVEn.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="MineCon2015", description="MineCon 2015 Cape")
async def min015(ctx: SlashContext):
        embed = discord.Embed(title="MineCon 2015", url="https://namemc.com/cape/72ee2cfcefbfc081", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="6732★", inline=False)
        embed.add_field(name= "How To Obtain", value="A redemption link for the cape was emailed to people attending minecon.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/72ee2cfcefbfc081)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/14QVUP2.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="MineCon2013", description="MineCon 2013 Cape")
async def min013(ctx: SlashContext):
        embed = discord.Embed(title="MineCon 2013", url="https://namemc.com/cape/0e4cc75a5f8a886d", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="6104★", inline=False)
        embed.add_field(name= "How To Obtain", value="A redemption link for the cape was emailed to people attending minecon.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/0e4cc75a5f8a886d)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/FxjT2Ll.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="MineCon2012", description="MineCon 2012 Cape")
async def min012(ctx: SlashContext):
        embed = discord.Embed(title="MineCon 2012", url="https://namemc.com/cape/ebc798c3f7eca2a3", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="3987★", inline=False)
        embed.add_field(name= "How To Obtain", value="A redemption link for the cape was emailed to people attending minecon.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/ebc798c3f7eca2a3)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/I2QgzGt.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="MineCon2011", description="MineCon 2011 Cape")
async def min011(ctx: SlashContext):
        embed = discord.Embed(title="MineCon 2011", url="https://namemc.com/cape/9349fa25c64ae935", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="3480★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was automatically added to all MINECON 2011 attendees' registered username.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/9349fa25c64ae935)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/T9aXsHI.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="RealmsMapMaker", description="Realms MapMaker Cape")
async def REALMS(ctx: SlashContext):
        embed = discord.Embed(title="Realms MapMaker", url="https://namemc.com/cape/11a3dcc4d826d0a1", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="315★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was automatically added to all MINECON 2011 attendees' registered username.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/11a3dcc4d826d0a1)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/Mah2xqS.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Mojang", description="Mojang Cape")
async def mojang(ctx: SlashContext):
        embed = discord.Embed(title="Mojang", url="https://namemc.com/cape/cb5dd34bee340182", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="204★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to employees of Mojang Studios. This design was used from October 7, 2015 to July 25, 2021.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/cb5dd34bee340182)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/P4iRwuG.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="MojangStudios", description="Mojang Studios Cape")
async def mojangstu(ctx: SlashContext):
        embed = discord.Embed(title="Mojang Studios", url="https://namemc.com/cape/c00df589ebea3ad6", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="103★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to employees of Mojang Studios. This design has been used since July 25, 2021. It was made by Johan Aronson and it resembles the Mojangs or gizmos that make up the Mojang Studios logo.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/c00df589ebea3ad6)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/CpDcyYa.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Translator", description="Translator Cape")
async def transla(ctx: SlashContext):
        embed = discord.Embed(title="Translator", url="https://namemc.com/cape/129a4675704fa3b8", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="88★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to some proofreaders (experienced translators with moderation permissions for their language) on the Minecraft translation project in Crowdin.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/129a4675704fa3b8)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/rTYFXy1.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Cobalt", description="Cobalt Cape")
async def Cobaltc(ctx: SlashContext):
        embed = discord.Embed(title="Cobalt", url="https://namemc.com/cape/696b6cc29946b968", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="18★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to participants/winners of level-making competitions and the Cobalt League tournaments in 2016.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/696b6cc29946b968)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/0zV2MRB.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Scrolls", description="Scrolls Cape")
async def Scrollsss(ctx: SlashContext):
        embed = discord.Embed(title="Scrolls", url="https://namemc.com/cape/116bacd62b233157", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="9★", inline=False)
        embed.add_field(name= "How To Obtain", value="Scrolls Cape	This cape was given to players who earned the Weekly First Place winner badge five times in Scrolls starting on November 7, 2014", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/116bacd62b233157)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/REJzbZL.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Turtle", description="Turtle Cape")
async def turtlec(ctx: SlashContext):
        embed = discord.Embed(title="Turtle", url="https://namemc.com/cape/8c05ef3c54870d04", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="3★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to billyK_ for his suggestion to add turtles into the game.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/8c05ef3c54870d04)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/SOjzoSt.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Valentine", description="Valentine Cape")
async def valentinec(ctx: SlashContext):
        embed = discord.Embed(title="Valentine", url="https://namemc.com/cape/3d528060ab734868", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="2★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to LolFoxy2 by a Mojang employee after resolving LolFoxy2's problems with migration to a Microsoft account. However, the cape was later removed after the Mojang employee realizing its rarity.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/3d528060ab734868)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/QRbfxP7.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Birthday", description="Birthday Cape")
async def birthdayc(ctx: SlashContext):
        embed = discord.Embed(title="Birthday", url="https://namemc.com/cape/aab5a23c7495fc70", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="1★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to Mojang employee Gr8Bizzo (formerly Gr8_Escape).", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/aab5a23c7495fc70)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/5hYslyk.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="dB", description="dB Cape")
async def dbc(ctx: SlashContext):
        embed = discord.Embed(title="dB", url="https://namemc.com/cape/77421d9cf72e07e9", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="1★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to dannyBstyle, a video game music composer, as Notch was a fan of his music.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/77421d9cf72e07e9)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/gRDQv0X.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Prismarine", description="Prismarine Cape")
async def dbcz(ctx: SlashContext):
        embed = discord.Embed(title="Prismarine", url="https://namemc.com/cape/88f1509813f4e324", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="1★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to Drullkus by Jeb for recreating the prismarine block for use in his Chisel mod rather than modifying Mojang's texture.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/88f1509813f4e324)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/cJDnpld.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Snowman", description="Snowman Cape")
async def dbccc(ctx: SlashContext):
        embed = discord.Embed(title="Snowman", url="https://namemc.com/cape/5e68fa78bd9df310", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="1★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to JulianClark in return for bringing Notch the TV presenter and actor Ray Cokes.", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/5e68fa78bd9df310)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/hrj9hlA.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(name="Spade", description="Spade Cape")
async def Spadec(ctx: SlashContext):
        embed = discord.Embed(title="Spade", url="https://namemc.com/cape/7a939dc1a7ad4505", color=0x19AC00)
        embed.set_author(name="Egglington", url="https://eggbot.site", icon_url="https://i.imgur.com/qrogvhd.png")
        embed.add_field(name= "Copies", value="1★", inline=False)
        embed.add_field(name= "How To Obtain", value="This cape was given to MrMessiah as a thank you for creating the BetterLight mod,", inline=False)
        embed.add_field(name= "Preview", value="Click [here](https://namemc.com/cape/7a939dc1a7ad4505)", inline=False)
        embed.set_footer(text="https://namemc.com/capes", icon_url = "https://i.imgur.com/VsCPCZY.png")
        embed.set_thumbnail(url="https://i.imgur.com/bYYta09.png")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

@slash.slash(
    name="daily",
    description="Claim your daily reward",
    options=[]
)
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    user_id = str(ctx.author.id)
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if not result:
        await ctx.send("You don't have any EggCoins yet. Start by using the /balance command.")
        return
    now = datetime.datetime.now()
    next_reset_time = now + datetime.timedelta(seconds=86400)
    cursor.execute("UPDATE user_reputation SET reputation = reputation + 5000 WHERE user_id = ?", (user_id,))
    conn.commit()
    await ctx.send(f"You have received 5000 EggCoins for your daily reward. Your new balance is {result[0] + 5000} EggCoins.")
    await ctx.send(f"Your next daily reward will be available on {next_reset_time.strftime('%Y-%m-%d %H:%M:%S')} UTC.")

@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Try again in {error.retry_after:.0f} seconds.")

@slash.slash(
    name="bet",
    description="Bet on a coin flip",
    options=[
        create_option(
            name="amount",
            description="Amount of EggCoins to bet",
            option_type=4,
            required=True
        ),
        create_option(
            name="choice",
            description="Choose 'Heads' or 'Tails'",
            option_type=3,
            required=True,
            choices=[
                create_choice(name="Heads", value="Heads"),
                create_choice(name="Tails", value="Tails")
            ]
        )
    ]
)
async def bet(ctx: SlashContext, amount: int, choice: str):
    user_id = str(ctx.author.id)
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if not result:
        await ctx.send("You don't have any EggCoins yet. Start by using the /balance command.")
        return
    reputation = result[0]
    if amount < 10:
        await ctx.send("You need a minimum of 10 EggCoins to place a bet.")
        return

    if amount > reputation:
        await ctx.send("You don't have enough EggCoins to make this bet.")
        return
    coin_flip = random.choice(["Heads", "Tails"])
    if coin_flip == choice:
        reputation_change = amount
        result_message = f"You chose {choice} and won! 🎉"
    else:
        reputation_change = -amount
        result_message = f"You chose {choice} and lost! 😞"
    cursor.execute("UPDATE user_reputation SET reputation = reputation + ? WHERE user_id = ?", (reputation_change, user_id))
    conn.commit()
    embed = discord.Embed(
        title="Coin Flip Result",
        description=f"{ctx.author.mention} bet {amount} EggCoins on the coin flip.",
        color=0x19AC00
    )
    embed.add_field(name="Coin Flip Result", value=f"The result is {coin_flip}. {result_message}", inline=False)
    embed.add_field(name="New Balance", value=f"Your new balance is {reputation + reputation_change} EggCoins.", inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/dSMCKNx.gif")
    await ctx.send(embed=embed)

@slash.slash(name="deepfry",
             description="Deepfries The Users Profile Picture",
             options=[
                 create_option(
                     name="member",
                     description="The Member you want to deepfry",
                     option_type=6,
                     required=True
                 )
             ])
async def deepfry(ctx: SlashContext, member: discord.Member = None):
    if member==None:
        member = ctx.message.author
    else:
        member = await bot.fetch_user(int(member.id))
    url1 = member.avatar_url_as(format="png")
    response = requests.get(f"https://nekobot.xyz/api/imagegen?type=deepfry&image={url1}")
    stuff = json.loads(response.text)
    embed = discord.Embed(title="DEEPFRY",
                          color=0x19AC00)
    embed.set_author(name="Egglington",
                     url="https://eggbot.site",
                     icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_footer(text="https://eggbot.site",
                     icon_url="https://i.imgur.com/qrogvhd.png")
    embed.set_image(url=stuff['message'])
    await ctx.send(embed=embed)
#//////////////////////////////////////////////////////////////////////////
def Init():
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    config.get('bottoken')
    try:
        bot.run(bottoken)
    except discord.errors.LoginFailure:
        input(f"{Fore.RED}[SYSTEM] BOT TOKEN IS INVALID CHECK CONFIG"+Fore.White)
        sys.exit
        python = sys.executable
        os.execl(python, python, * sys.argv)
Init()
