import asyncio
import json
import sqlite3
import datetime
import logging

import discord
import requests

from discord.ext import commands

from collections import defaultdict
from iniconfig import IniConfig
from psutil import (
    cpu_percent, getloadavg, virtual_memory, cpu_count,
    cpu_freq, disk_partitions, disk_usage,
)
from GPUtil import getGPUs
from regex import regex as re

import platy_sec.sec_main as sec
from platy_sec.stalker import (
    smessage, smessage_edit, smessage_delete,
)

from commands.commonc import makepet, handle_dick
from commands.clone_guild import clone_guild
from commands.suggest import process_suggestion
from commands.cat import handle_cat_command

from functions.unmute import unmute
from functions.commonf import handle_ping


ESC: str = "\u001b"
COLORS: dict[str, str] = {
    "RED": f"{ESC}[1;31m",
    "GREEN": f"{ESC}[1;32m",
    "YELLOW": f"{ESC}[1;33m",
    "BLUE": f"{ESC}[1;34m",
    "MAGENTA": f"{ESC}[1;35m",
    "CYAN": f"{ESC}[1;36m",
    "WHITE": f"{ESC}[1;37m",
    "RESET": f"{ESC}[0m",
}


# Konfigurationsdatei laden
conn = sqlite3.connect("user_data.db")
c = conn.cursor()

config = IniConfig("config.ini")
prefix = config.get("config", "prefix")
TOKEN = config.get("config", "token")
SUGG_WEBHOOK_URL = config.get("config", "sugg_webhook_url")
ABUSEIPDB = config.get("config", "abuseipdb_key")
STALKUSERS = config.get("config", "stalk_users")
BANNED_GUILDS = config.get("config", "banned_guilds")

# Database-Initialisierung
c.execute('''
CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    suggestion TEXT NOT NULL,
    date TEXT NOT NULL
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT NOT NULL,
    username TEXT NOT NULL,
    admin_privileges INTEGER NOT NULL
)
''')

# Function to add a suggestion


def add_suggestion(user, suggestion):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''
    INSERT INTO suggestions (user, suggestion, date)
    VALUES (?, ?, ?)
    ''', (user, suggestion, date))
    conn.commit()

# Function to add a permission


def add_permission(userid, username, admin_privileges):
    c.execute('''
    INSERT INTO permissions (userid, username, admin_privileges)
    VALUES (?, ?, ?)
    ''', (userid, username, admin_privileges))
    conn.commit()


def get_admin_privileges(userid):
    c.execute('''
    SELECT admin_privileges FROM permissions WHERE userid = ?
    ''', (userid,))
    return c.fetchone()


def get_owner():
    guild_id: int = 1009281888118120528
    guild: discord.Guild = bot.get_guild(guild_id)
    if guild is not None:
        return guild.owner
    else:
        print(f"Couldn't find guild/owner!!!  {guild}")


def log(logmsg):
    print(logmsg)


# Initialize a counter to track the number of "dick" requests per user
dick_counter = defaultdict(int)

# Bot-Initialisierung
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix.lower()))

# Ereignis, wenn der Bot bereit ist


@bot.event
async def on_ready():
    log(f"""Logged in as {bot.user.name}{f'#{bot.user.discriminator}' if bot.user.discriminator != "0" else ""}
    - ID: {bot.user.id}
    - Prefix: {prefix}
    - Created at {bot.user.created_at.date()}
    - Servers: {len(bot.guilds)}
    - MFA: {bot.user.mfa_enabled}
    - Verified: {bot.user.verified}
    - badges = {[badge[0] for badge in bot.user.public_flags.all()]}""")

    owner = None
    owner = get_owner()

    log(f"""Bot-Owner: {owner.name}{f'#{owner.discriminator}' if owner.discriminator != "0" else ""}
    - ID: {owner.id}
    - Created at {owner.created_at.date()}
    - badges = {[badge[0] for badge in owner.public_flags.all()]}""")
    return owner


# Funktion, um Vorschläge in eine Textdatei zu speichern

"""
Handles the event when a member's voice state is updated.

Args:
    member: The discord.Member whose voice state was updated.
    before: The previous voice state of the member.
    after: The new voice state of the member.

Returns:
    None
"""


@bot.event
@commands.has_permissions(mute_members=True)
@commands.has_permissions(deafen_members=True)
async def on_voice_state_update(member: discord.Member, before: any, after: any) -> None:
    await unmute(member, before, after)

"""
Handles the suggest command to add a suggestion and process it.

Args:
    ctx: The context of the command.
    suggestion: The suggestion provided by the user.

Returns:
    None
"""


@bot.command()
async def suggest(ctx, *, suggestion):

    if str(ctx.guild.id) not in BANNED_GUILDS:
        await add_suggestion(ctx.author.name, suggestion)
        await process_suggestion(ctx, suggestion, SUGG_WEBHOOK_URL)


"""
Handles the event when a message is received.

If the message content matches a Discord Nitro gift link pattern, it is written to a file 'nitro.txt'.
If the message content does not match the pattern, the message is processed as a command.

Args:
    message: The message received.

Returns:
    None
"""


@bot.event
async def on_message(message: discord.Message):
    if re.match(r"(https://)?(discord\.(gift|com/gifts)/)[a-zA-Z0-9]+", message.content):
        with open("nitro.txt", "a") as f:
            f.write(message.content)
            f.truncate()
            f.close()

    elif str(message.channel.guild.id) not in BANNED_GUILDS:
        if message.channel.guild.id is None:
            print(message)
        else:
            await bot.process_commands(message)
    await smessage(get_owner(), STALKUSERS, message)


@bot.event
async def on_message_edit(before, after):
    await smessage_edit(get_owner(), STALKUSERS, before, after)


@bot.event
async def on_message_delete(message):
    await smessage_delete(get_owner(), STALKUSERS, message)


@bot.command(name="ping")
async def ping(ctx):
    await handle_ping(ctx, bot, BANNED_GUILDS)


"""
Handles the pet command to create a 'petpet' animation of a user's avatar.

Args:
    ctx: The context of the command.
    user: The user whose avatar will be animated (default is None).

Returns:
    None
"""


@bot.command(name="pet", aliases=["pat", "patpat", "petpet"])
async def pet(ctx, user: discord.User = None):
    await makepet(ctx, user)

"""
Handles the load command to display system information including CPU usage, load, RAM usage, CPU cores, CPU frequency, battery percentage, disk information, and GPU information.

Args:
    ctx: The context of the command.

Returns:
    None
"""


@bot.command()
async def load(ctx: commands.Context) -> None:
    """
    Get the system load.

    Parameters:
    - ctx: The context object representing the invocation context.

    Returns:
    None
    """
    disk_part = disk_partitions()
    gpu = getGPUs()
    disks = []
    for disk in disk_part:
        disk_letter = disk.device.split(":")[0]
        disks.append(f"{disk_letter}")
    load_message = "```ansi\n"
    load_message += f"{COLORS['MAGENTA']}CPU:{COLORS['RESET']}\n"
    load_message += f"    {COLORS['CYAN']}Usage:{COLORS['RESET']} {cpu_percent()}%\n"
    load_message += f"    {COLORS['CYAN']}Load:{COLORS['RESET']} {getloadavg()}\n"
    load_message += f"    {COLORS['CYAN']}Cores:{COLORS['RESET']} {cpu_count()}\n"
    load_message += f"    {COLORS['CYAN']}Frequency:{COLORS['RESET']} {round(cpu_freq().current / 1000,2)}GHz\n"
    load_message += f"{COLORS['MAGENTA']}RAM:{COLORS['RESET']}\n"
    load_message += (
        f"    {COLORS['CYAN']}Usage:{COLORS['RESET']} {virtual_memory().percent}%\n"
    )
    load_message += f"    {COLORS['CYAN']}Total:{COLORS['RESET']} {round(virtual_memory().total / 1024 / 1024 / 1024)}GB\n"
    load_message += f"    {COLORS['CYAN']}Used:{COLORS['RESET']} {round(virtual_memory().used / 1024 / 1024 / 1024,2)}GB\n"
    load_message += f"    {COLORS['CYAN']}Free:{COLORS['RESET']} {round(virtual_memory().free / 1024 / 1024 / 1024,2)}GB\n"
    if gpu:
        gpu_ram = round(gpu[0].memoryTotal / 1024)
        gpu_ram_used = round(gpu[0].memoryUsed / 1024)
        temp = gpu[0].temperature
        gpu = gpu[0]
        load_message += f"{COLORS['MAGENTA']}GPU:{COLORS['RESET']}\n"
        load_message += f"    {COLORS['CYAN']}Name:{COLORS['RESET']} {gpu.name}\n"
        load_message += f"    {COLORS['CYAN']}RAM:{COLORS['RESET']} {gpu_ram}GB\n"
        load_message += (
            f"    {COLORS['CYAN']}RAM Used:{COLORS['RESET']} {gpu_ram_used}GB\n"
        )
        load_message += (
            f"    {COLORS['CYAN']}Temperature:{COLORS['RESET']} {temp}°C\n"
        )
        load_message += f"{COLORS['MAGENTA']}Disks:{COLORS['RESET']}\n"
    for disk in disks:
        load_message += f"    {COLORS['BLUE']}Disk {disk}:{COLORS['RESET']}\n"
        load_message += f"        {COLORS['CYAN']}Usage:{COLORS['RESET']} {disk_usage(f'{disk}:// ').percent}%\n"
        load_message += f"        {COLORS['CYAN']}Total:{COLORS['RESET']} {round(disk_usage(f'{disk}://').total / 1024 / 1024 / 1024)}GB\n"
        load_message += f"        {COLORS['CYAN']}Used:{COLORS['RESET']} {round(disk_usage(f'{disk}://').used / 1024 / 1024 / 1024,2)}GB\n"
    load_message += "```"
    if str(ctx.guild.id) not in BANNED_GUILDS:
        async with ctx.typing():
            await ctx.send(load_message)


@bot.command()
async def dick(ctx, arg: int):
    await handle_dick(ctx, arg, dick_counter)


#
#
@bot.command()
async def cat(ctx):
    await handle_cat_command(ctx, "cat")


@bot.command()
async def cif(ctx):
    await handle_cat_command(ctx, "cif")


@bot.command()
async def meow(ctx, *, text=None):
    await handle_cat_command(ctx, "meow", text)

"""
Handles the safeip command to check the abuse confidence score and Tor status of an IP address using the 'abuseipdb' API.
TODO:addvirustotal

Args:
    ctx: The context of the command.
    ip: The IP address to check.

Returns:
    None
"""
# just a idea not really that important its just looks in abuseipdb for the confidentscore and if its a tor ip would be better with virustotal api but i didnt had a api key for it


@bot.command()
async def safeip(ctx, ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '365'
    }
    headers = {
        'Accept': 'application/json',
        'Key': ABUSEIPDB
    }
    r = requests.request(method='GET', url=url,
                         headers=headers, params=querystring)
    decodedResponse = json.loads(r.text)
    confidentscore = decodedResponse["data"]["abuseConfidenceScore"]
    isTor = decodedResponse["data"]["isTor"]
    await ctx.send(f"TorIP:  {isTor}\nConfidentscore:  {confidentscore}/100")

"""
Handles the addadmin command to grant admin privileges to a user.

Args:
    ctx: The context of the command.
    user: The user to grant admin privileges.

Returns:
    None
"""


@bot.command()
async def addadmin(ctx, user: discord.User):
    if get_admin_privileges(ctx.author.id)[0] == 1:
        add_permission(user.id, user.name, 1)
        await ctx.send("Added succesfully")
    else:
        await ctx.send("Du hast keine Berechtigungen dafür")

"""
Handles the removeadmin command to revoke admin privileges from a user.

Args:
    ctx: The context of the command.
    user: The user to revoke admin privileges from.

Returns:
    None
"""


@bot.command()
async def removeadmin(ctx, user: discord.User):
    if get_admin_privileges(ctx.author.id)[0] == 1:
        add_permission(user.id, user.name, 0)
        await ctx.send("Removed succesfully")
    else:
        await ctx.send("Du hast keine Berechtigungen dafür")

"""
Handles the timeout command to apply a timeout to a user in the guild.

Args:
    ctx: The context of the command.
    time: The duration of the timeout.
    user: The user to apply the timeout to.
    reason: The reason for the timeout.

Returns:
    None
"""


@bot.command()
@commands.has_guild_permissions(moderate_members=True)
async def timeout(ctx, time=None, *, user: discord.Member, reason=None):

    await ctx.send(f"time:\n```{time}```\nreason:\n```{reason}```\n")
    await user.timeout(time, reason)
    await ctx.send(
        f"Timed out **{user.name}**.\n*Reason*: ```{reason}```\n*Duration*: ```{time}```")

    # https://discordpy-self.readthedocs.io/en/latest/api.html?highlight=timeout#discord.Member.timeout


@bot.command(name="clone", help="Clone a server and applies it to another server.")
async def clone(ctx, clone_from: int, clone_to: int) -> None:
    await clone_guild(ctx, clone_from, clone_to, bot)


# Clear before start
# bot.http.clear()

# Bot starten
bot.run(TOKEN)
