import discord
import requests
import json
import sqlite3
import datetime


from discord.ext import commands
from iniconfig import IniConfig
from io import BytesIO
from psutil import cpu_percent, getloadavg, virtual_memory, cpu_count, cpu_freq, sensors_battery, disk_partitions
from GPUtil import getGPUs
from petpetgif import petpet
from regex import regex as re

from commands.clone_guild import clone_guild
from commands.suggest import process_suggestion
from functions.unmute import unmute


# Konfigurationsdatei laden
conn = sqlite3.connect("user_data.db")
c = conn.cursor()

config = IniConfig("config.ini")
prefix = config.get("config", "prefix")
TOKEN = config.get("config", "token")
SUGG_WEBHOOK_URL = config.get("config", "sugg_webhook_url")
ABUSEIPDB = config.get("config", "abuseipdb_key")

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


# Bot-Initialisierung
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix.lower()))

# Ereignis, wenn der Bot bereit ist


@bot.event
async def on_ready():
    print(f"Successfully logged in as {bot.user.name}.")

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
    add_suggestion(ctx.author.name, suggestion)
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
async def on_message(message):
    if re.match(r"(https://)?(discord\.(gift|com/gifts)/)[a-zA-Z0-9]+", message.content):
        with open("nitro.txt", "a") as f:
            f.write(message.content)
            f.truncate()
            f.close()
    else:
        await bot.process_commands(message)


"""
Handles the ping command to measure the bot's latency and respond with a 'Pong!' message.

Args:
    ctx: The context of the command.

Returns:
    None
"""


@bot.command()
async def ping(ctx):
    calc = round(bot.latency * 1000, 1)
    await ctx.send(f"Pong! {calc}ms")

"""
Handles the test command to display a test message with two arguments.

Args:
    ctx: The context of the command.
    arg: The first argument.
    arg2: The second argument.

Returns:
    None
"""


@bot.command()
async def test(ctx, arg, arg2):
    await ctx.send(f"Test: {arg} {arg2}")

"""
Handles the pet command to create a 'petpet' animation of a user's avatar.

Args:
    ctx: The context of the command.
    user: The user whose avatar will be animated (default is None).

Returns:
    None
"""


@bot.command()
async def pet(ctx, user: discord.User = None):
    try:
        await ctx.message.delete()
    except discord.ext.commands.errors.CommandInvokeError:
        print("Error deleting message containing command")
    except discord.errors.Forbidden:
        print("Error deleting message (2FA)")

    if user is None:
        avatar = await ctx.author.avatar.read()
    else:
        avatar = await user.avatar.read()
    source = BytesIO(avatar)
    dest = BytesIO()
    petpet.make(source, dest)
    dest.seek(0)
    await ctx.send(file=discord.File(dest, filename=f"{avatar[0]}-petpet.gif"))

"""
Handles the load command to display system information including CPU usage, load, RAM usage, CPU cores, CPU frequency, battery percentage, disk information, and GPU information.

Args:
    ctx: The context of the command.

Returns:
    None
"""


@bot.command()
async def load(ctx):
    if get_admin_privileges(ctx.author.id)[0] != 1:
        return
    disk_part = disk_partitions()
    gpu = getGPUs()
    disks = []
    for disk in disk_part:
        disk_letter = disk.device.split(":")[0]
        disks.append(f"{disk_letter}")
    if gpu:
        gpu_ram = round(gpu[0].memoryTotal / 1024)
        gpu_ram_used = round(gpu[0].memoryUsed / 1024)
        temp = gpu[0].temperature
        gpu = gpu[0]
        await ctx.send(f"CPU: {cpu_percent(interval=1)}%\nLoad: {getloadavg()}\nRAM: {round(virtual_memory().total / (1024 ** 3),2)}GB\nRAM Load: {int(virtual_memory().percent)}%\nCPU Cores: {cpu_count()}\nCPU Frequency: {round(cpu_freq().current / 1000,2)}GHz\nBattery: {sensors_battery()}%\nDisks: {disks}\nGPU: {gpu.name}\nGPU RAM: {gpu_ram}GB\nGPU RAM Used: {gpu_ram_used}GB\nGPU Temp: {temp}°C")
    else:
        await ctx.send(f"CPU: {cpu_percent(interval=1)}%\nLoad: {getloadavg()}\nRAM: {round(virtual_memory().total / (1024 ** 3),2)}GB\nRAM Load: {int(virtual_memory().percent)}%\nCPU Cores: {cpu_count()}\nCPU Frequency: {round(cpu_freq().current / 1000,2)}GHz\nBattery: {sensors_battery()}%\nDisks: {disks}")

"""
Handles the dick command to generate a visual representation of a 'dick' with a specified length.

Args:
    ctx: The context of the command.
    arg: The length of the 'dick' represented by the number of '=' characters.

Returns:
    None
"""


@bot.command()
async def dick(ctx, arg: int):
    shaft = "=" * arg
    await ctx.send(f"8{shaft}B")

"""
Handles the cat command to display a random cat image from the 'cataas' API.

Args:
    ctx: The context of the command.

Returns:
    None
"""


@bot.command()
async def cat(ctx):
    url = "https://cataas.com/cat?type=medium"
    await ctx.send(url)

"""
Handles the cif command to display a random cat GIF from the 'cataas' API.

Args:
    ctx: The context of the command.

Returns:
    None
"""


@bot.command()
async def cif(ctx):
    url = "https://cataas.com/cat/gif?type=medium"
    await ctx.send(url)

"""
Handles the meow command to display a cat image with optional text using the 'cataas' API.

Args:
    ctx: The context of the command.
    text: Optional text to display on the cat image (default is None).

Returns:
    None
"""


@bot.command()
async def meow(ctx, *, text=None):
    if text is None:
        url = "https://cataas.com/cat/says/hehe?fontSize=50&fontColor=violet"
    else:
        url = f"https://cataas.com/cat/says/{text}?fontSize=50&fontColor=violet"
    await ctx.send(url)

"""
Handles the safeip command to check the abuse confidence score and Tor status of an IP address using the 'abuseipdb' API.
TODO:move api key+addvirustotal

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
    # temporary aslong as Gabriel didnt added it to config.ini
    ABUSEIPDB = "1e6cf48ee828259d88c533d1576303e454cb00319033f4bd32237a66124477b60bfb989c93aa8a27"
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
        await ctx.send("removed succesfully")
    else:
        await ctx.send("du hast keine berechtigungen dafür")

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


# Bot starten
bot.run(TOKEN)
